from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import get_settings
from app.models.user import UserRole, TokenData
from app.database import get_db

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ─── Token Verify ────────────────────────────────────
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("user_id")
        role: str = payload.get("role")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id, role=role)

    except JWTError:
        raise credentials_exception

    # DB se user fetch karo
    db = get_db()
    from bson import ObjectId
    user = await db.users.find_one({
        "_id": ObjectId(token_data.user_id),
        "status": "active"
    })

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return user


# ─── Role Check Dependencies ─────────────────────────
async def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def require_analyst(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in [UserRole.ANALYST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analyst or Admin access required"
        )
    return current_user


async def require_viewer(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in [UserRole.VIEWER, UserRole.ANALYST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Login required"
        )
    return current_user