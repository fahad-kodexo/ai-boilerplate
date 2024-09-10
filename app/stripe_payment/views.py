from app.utils.responses import success_response, error_response, not_found_response
from app.utils.constants import STRIPE_KEY, ENDPOINT_SECRET, SUCCESS_URL
from app.utils.stripe_utils import Customer
from fastapi.templating import Jinja2Templates
from app.stripe_payment.db import UserPayment
from typing import Optional
from starlette.requests import Request
from fastapi import Header
from . import schemas
import stripe
import traceback

stripe.api_version = "2020-08-27"
stripe.api_key = STRIPE_KEY
endpoint_secret = ENDPOINT_SECRET

templates = Jinja2Templates(directory="app/templates")


async def create_checkout_session(
    request: Request, checkout_session: schemas.CheckoutSession
):
    try:
        checkout_session = stripe.checkout.Session.create(
            customer=checkout_session.customer_id,
            success_url=SUCCESS_URL,
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {"price": checkout_session.price_id, "quantity": 1},
            ],
        )
        response = {
            "sessionId": checkout_session["id"],
            "sessionUrl": checkout_session["url"],
        }
        return success_response(response)
    except Exception as e:
        print(traceback.print_exc())
        error_response(repr(e))


async def webhook(
    request_data: Request, stripe_signature: Optional[str] = Header(None)
):
    try:
        payload = await request_data.body()

        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=stripe_signature, secret=endpoint_secret
        )

        if event.type == "checkout.session.completed":
            event_data = event.data
            customer_id = event_data.object.get("customer")
            await UserPayment().update_user_status(customer_id, "Payment Succeeded")

        elif event.type == "customer.subscription.deleted":
            event_data = event.data
            customer_id = event_data.object.get("customer")
            await UserPayment().update_user_status(customer_id, "Subscription Deleted")

        elif event.type == "invoice.payment_succeeded":
            event_data = event.data
            customer_id = event_data.object.get("customer")
            if event_data.object.get("billing_reason") == "subscription_cycle":
                await UserPayment().update_user_status(
                    customer_id, "Invoice Payment Succeeded", payment_cycle=True
                )
            else:
                await UserPayment().update_user_status(
                    customer_id, "Invoice Payment Succeeded"
                )

        elif event.type == "payment_intent.succeeded":
            event_data = event.data
            customer_id = event_data.object.get("customer")
            await UserPayment().update_user_status(
                customer_id, "Payment Intent Succeeded"
            )

        elif event.type == "customer.subscription.updated":
            event_data = event.data
            customer_id = event_data.object.get("customer")
            await UserPayment().update_user_status(
                customer_id, "Customer Subscription Updated"
            )
        else:
            print(f"Unhandled event type {event.type}")

        return success_response("Handled Event Successfully")

    except Exception as e:
        print(traceback.print_exc())
        return error_response(repr(e))


async def create_portal_session(
    request: Request, portal_session: schemas.PortalSession
):
    try:
        return_url = SUCCESS_URL
        checkout_session_id = portal_session.session_id
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

        portal_session = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=return_url,
        )
        response = {"sessionUrl": portal_session["url"]}
        return success_response(msg="Portal Session Found", data=response)
    except Exception as e:
        print("Error in create_portal_session", e)
        return error_response(repr(e))


async def create_customer(customer: schemas.Customer):
    try:
        customer_id = Customer.create_customer(
            name=customer.name, email=customer.email
        ).get("id")

        if customer_id is None:
            raise Exception

        await UserPayment().insert_user_payment(
            customer_id, "Customer Created", customer.email
        )
        return success_response(
            msg="Customer Created", data={"customer_id": customer_id}
        )
    except Exception as e:
        print("Error in create_customer", e)
        return error_response(repr(e))


def checkout_success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})
