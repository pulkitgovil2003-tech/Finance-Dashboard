from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate
from app.utils.response import success_response, failure_response
from app.services.auth_service import AuthService
from app.middleware.auth_middleware import get_current_user
from app.database import get_db

router = APIRouter(prefix="/api/auth", tags=["Auth"])


# ─── Register ────────────────────────────────────────
@router.post("/register")
async def register(user_data: UserCreate):
    db = get_db()
    auth_service = AuthService(db)

    try:
        user = await auth_service.register(user_data)
        return success_response(
            message="User registered successfully",
            data={
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        )
    except ValueError as e:
        return failure_response(message=str(e))
    except Exception as e:
        return failure_response(message="Something went wrong")


# ─── Login ───────────────────────────────────────────
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    auth_service = AuthService(db)

    try:
        result = await auth_service.login(form_data.username, form_data.password)
        return success_response(
            message="Login successful",
            data=result
        )
    except ValueError as e:
        return failure_response(message=str(e))
    except Exception as e:
        return failure_response(message="Something went wrong")


# ─── Me ──────────────────────────────────────────────
@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    try:
        return success_response(
            message="User fetched successfully",
            data={
                "id": str(current_user["_id"]),
                "name": current_user["name"],
                "email": current_user["email"],
                "role": current_user["role"],
                "status": current_user["status"]
            }
        )
    except Exception as e:
        return failure_response(message="Something went wrong")