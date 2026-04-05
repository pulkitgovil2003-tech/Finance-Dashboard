from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from bson import ObjectId
from app.config import get_settings
from app.models.user import UserCreate, UserRole, UserStatus

settings = get_settings()

# ─── Password Hashing ────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ─── JWT Token ───────────────────────────────────────
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


# ─── Auth Service Class ──────────────────────────────
class AuthService:
    def __init__(self, db):
        self.db = db

    async def register(self, user_data: UserCreate) -> dict:
        # Email already exists check
        existing = await self.db.users.find_one({"email": user_data.email})
        if existing:
            raise ValueError("Email already registered")

        # Pehla user admin banega automatically
        user_count = await self.db.users.count_documents({})
        role = UserRole.ADMIN if user_count == 0 else user_data.role

        # User document banana
        user_doc = {
            "name": user_data.name,
            "email": user_data.email,
            "password": hash_password(user_data.password),
            "role": role,
            "status": UserStatus.ACTIVE,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = await self.db.users.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return user_doc

    async def login(self, email: str, password: str) -> dict:
        # User dhundo
        user = await self.db.users.find_one({"email": email})
        if not user:
            raise ValueError("Invalid email or password")

        # Password check
        if not verify_password(password, user["password"]):
            raise ValueError("Invalid email or password")

        # Status check
        if user["status"] != UserStatus.ACTIVE:
            raise ValueError("Account is inactive, contact admin")

        # Token banao
        token = create_access_token({
            "user_id": str(user["_id"]),
            "role": user["role"]
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "status": user["status"]
            }
        }