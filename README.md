# Stripe Press Book Store

This is a demo ecommerce application for purchasing a book using Stripe’s Payment Element and the PaymentIntents API.

The application lets a customer:
1. Select a book from the catalog.
2. Complete a card payment using Stripe’s embedded Payment Element.
3. View a confirmation page with the charged amount and Stripe's PaymentIntent ID.

## Part 1: How to build, configure and run your application.

## Prerequisites

- Python 3.9 or later
- A Stripe account (in test mode)
- Stripe Account's test API keys

## Setup and configuration

-  Complete the creation and setup of a free test account [here](https://dashboard.stripe.com/register)). You'll need a set of testmode API keys from the Stripe dashboard later.

- Clone the repository and enter the project directory:
bash git clone <repository-url>
cd sa-takehome-project-python

- Create and activate a virtual environment:
bash python3 -m venv .venv source .venv/bin/activate

- Install dependencies:
bash python -m pip install --upgrade pip python -m pip install -r requirements.txt


- Create a `.env` file in the project root:
env STRIPE_SECRET_KEY=sk_test_... STRIPE_PUBLISHABLE_KEY=pk_test_...

Use test keys for local development. You can retrieve test keys from your dashboard using this [link](https://dashboard.stripe.com/test/apikeys)

- Run the application:
bash python app.py
Navigate to [http://localhost:5000](http://localhost:5000) to view the index page.

## Testing a payment

1. Select a book from the catalog by clicking on 'Purchase'.
2. Enter an email address on checkout page.
3. Enter Stripe’s test card details. You can use the ones below:
Card number: 4242 4242 4242 4242
Expiration: Any future date
CVC: Any three digits
4. Submit the payment.
5. Confirm that the success page displays the total amount charged and a PaymentIntent ID beginning with `pi_`.
6. (Optionally) verify the payment in your Stripe Dashboard while viewing test-mode data.

## Part 2: How does the solution work? Which Stripe APIs does it use? How is this application architected?

## Application Architecture
The application has three main parts:

1. [Flask](https://flask.palletsprojects.com/) backend
Stores the book catalog in the server-side BOOKS dictionary.
Renders the catalog, checkout, and success pages.
Creates and retrieves PaymentIntents using Stripe’s secret API key.
Determines prices on the server, so the browser cannot modify the amount charged.

2. Browser checkout page
Displays the selected book, its server-rendered price, and an email field.
Loads Stripe.js
Mounts Stripe’s Payment Element, which securely collects card details without card data passing through the application.
Confirms the PaymentIntent using stripe.confirmPayment(...).

3. Stripe
Handles secure collection and confirmation of card details through the Payment Element.
Processes the payment.
Returns the final payment status and the PaymentIntent ID.

## Outline of the Payment flow

1. The customer selects a book from the catalog.
2. Flask renders checkout using the server-side book catalog.
3. The browser sends the selected item ID to `POST /create-payment-intent`.
4. Flask looks up the item and creates a PaymentIntent for the amount.
5. Flask returns the PaymentIntent client secret.
6. Stripe.js uses the client secret to mount the Payment Element.
7. The customer submits payment through `stripe.confirmPayment(...)`.
8. Flask retrieves and verifies the successful PaymentIntent before rendering the success page.

## Stripe Products and APIs used
- [Stripe Payment Element](https://docs.stripe.com/js/element/payment_element) securely collects card details in Stripe-hosted UI components.
- [Stripe.js](https://docs.stripe.com/js) initializes and confirms the Payment Element.
- [PaymentIntents API](https://docs.stripe.com/api/payment_intents ) creates, confirms, and retrieves payment state.


## Part3: How was this problem approached? Which docs were used to complete the project? What challenges were encountered?
## Approach
Starting with the available boilerplate code, a minimal payment flow has been added around the existing checkout and success pages, without comitting to database use or frontend improvements.
The key focus was achieving the assignment stipulated objectives without adding complexity.


## Docs
I heavily relied on the following docs to gain in-depth understanding of the Payment Element flow & utilized the Quickstart guide and GitHub Sample to build this demo:
1. Understanding [Payment Elements](https://docs.stripe.com/payments/payment-element)
2. Stripe doc on [Accept a Payment](https://docs.stripe.com/payments/accept-a-payment?payment-ui=elements&api-integration=paymentintents)
3. Build a checkout page [Quickstart Guide](https://docs.stripe.com/payments/quickstart?lang=python) with PaymentIntents API
4. [Github Sample](https://github.com/stripe-samples/accept-a-payment/tree/main/payment-element/server/python) using Payment Element

## Challenges
1. Configuration issue with Flask 2.0.0 and Werkzeug compatibility - The required Werkzeug version is now added to `requirements.txt` so setup is reproducible.
2. A multitude of syntax errors and library issues
    2.a jsonify import error
    2.b Payment Element failed to load due to missing attribute id for payment-form and submit-button.
    2.c Syntax issues due to route decorator and the def it decorates not starting in the same column.
3. Use of paymentMethodOrder did not change the order of appearance of payment methods (Link surface still appears before card).


## Part 4: How can the same application be extended to build a more robust instance of the same?
The simplified demo app can be made more robust by adding the following features:
1. Refine payment flow to defer creating PI before submission [Two step confirmation](https://docs.stripe.com/payments/build-a-two-step-confirmation)
2. Adding authentication (3DS)
3. Collect shipping details
4. Adaptive pricing & Multi-currency support
5. Save card for future use
6. Offer wallets and LPMs
7. Use of Appearance API
8. Handle failure scenarios cleanly
9. Use webhooks
10. Use database