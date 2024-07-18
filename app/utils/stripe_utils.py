import stripe
from app.utils.constants import STRIPE_KEY

stripe.api_key = STRIPE_KEY

payment_method = {"enabled": True}

class Customer:
    @staticmethod
    def create_customer(name:str,email:str):
        try:
            return stripe.Customer.create(
            name=name,
            email=email,
            )
        except Exception as e:
            print("Exception in create_customer",e)
            return None

    @staticmethod
    def retrieve_customer(customer_id:str):
        try:
            return stripe.Customer.retrieve(customer_id)
        except Exception as e:
            print("Exception in retrieve_customer",e)
            return None

    @staticmethod
    def list_all_customers():
        try:
            return stripe.Customer.list()
        except Exception as e:
            print("Exception in list_all_customers",e)
            return None

class Payment:
    @staticmethod
    def create_payment_intent(amount:int,currency:str,customer_id:str):
        try:
            return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            customer = customer_id,
            automatic_payment_methods= payment_method
            )
        except Exception as e:
            print("Exception in creatE_payment_intent",e)
            return None

    @staticmethod
    def retrieve_payment(payment_id:str):
        try:
            return stripe.PaymentIntent.retrieve(payment_id)
        except Exception as e:
            print("Exception in retrieve_payment",e)
            return None

    @staticmethod
    def list_all_payments():
        try:
            return stripe.PaymentIntent.list()
        except Exception as e:
            print("Error in list_all_payments",e)
            return None
