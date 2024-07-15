from fastapi import APIRouter

from .views import (webhook,
                    create_checkout_session,
                    create_portal_session,
                    create_customer,
                    checkout_success)

stripe_router = APIRouter(prefix="/stripe")

stripe_router.post("/webhook")(webhook)
stripe_router.post('/create_checkout_session')(create_checkout_session)
stripe_router.post('/create_portal_session')(create_portal_session)
stripe_router.post("/create_customer")(create_customer)
stripe_router.get('/checkout_success')(checkout_success)
