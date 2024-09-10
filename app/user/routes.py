from fastapi import APIRouter

from .views import (
    register_user,
    login_user,
    forget_password,
    verify_otp,
    reset_password,
)

auth_router = APIRouter(prefix="/user")

auth_router.post("/register")(register_user)
auth_router.post("/login")(login_user)
auth_router.post("/forget_password")(forget_password)
auth_router.post("/reset_password")(reset_password)
auth_router.post("/verify_otp")(verify_otp)
