import os
import stripe

from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()

# Environment variable for API key
# Only test keys are used in this example
# API keys are loaded from requirements.txt
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

#Catalogue for books, hardcoded to avoid use of a database in this app
#Amounts are stored in integer cents, as required by the Stripe API
BOOKS = {
  '1': {
    'title': 'The Art of Doing Science and Engineering',
    'amount': 2300
  },
  '2': {
    'title': 'The Making of Prince of Persia: Journals 1985-1993',
    'amount': 2500
  },
  '3': {
    'title': 'Working in Public: The Making and Maintenance of Open Source',
    'amount': 2800
  }
}


app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))

# Home route
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():

  item = request.args.get('item')

  # Look up the selected book on the server before rendering its checkout page.
  book = BOOKS.get(item)
  title = None
  amount = None
  error = None

  if book:
    title = book['title']
    amount = book['amount']
  else:
  # Included in layout view, feel free to assign error
    error = 'No item selected'
  #The publishable key is safe to expose to Stripe.js in the browser
  return render_template('checkout.html', title=title, amount=amount, error=error, item=item, publishable_key=os.getenv('STRIPE_PUBLISHABLE_KEY'))

#Create PaymentIntent route
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
  data = request.get_json(silent=True) or {}
  item = data.get('item')
  # The browser submits only the item ID. This is done to avoid trusting a client submitted amount.
  book = BOOKS.get(item)

  if not book:
    return jsonify(error='Invalid book selection'), 400
  amount = book['amount']

  try:
    # Create an unconfirmed PaymentIntent for the Payment Element to confirm.
    payment_intent = stripe.PaymentIntent.create(
      amount=amount,
      currency='usd',
      # payment_method_types=['card'] (This limits automatic payment method selection such as for Link.)
      automatic_payment_methods={
        'enabled': True
      }
    )
  except stripe.error.StripeError:
    return jsonify(error='Unable to create payment'), 400

  # Stripe.js uses the client secret to initialize the Payment Element.
  # The secret API key remains on the server.
  return jsonify(
    clientSecret=payment_intent.client_secret
  )

# Success route
@app.route('/success', methods=['GET'])
def success():
  payment_intent_id = request.args.get('payment_intent')
  amount = None
  error = None

  if not payment_intent_id:
    error = 'No payment was supplied'
  else:
    try:
      # Retrieve the PaymentIntent from server-side and verify its final status.
      payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

      if payment_intent.status == 'succeeded':
         # Use verified amount from payment intent object rather than a value from the browser.
        amount = payment_intent.amount
      else:
        error = 'The payment has not succeeded'
    except stripe.error.StripeError:
      error = 'The payment could not be found'
  return render_template('success.html', amount=amount, payment_intent_id=payment_intent_id, error=error)


if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)