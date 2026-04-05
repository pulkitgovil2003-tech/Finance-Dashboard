from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from bson import ObjectId
from app.config import get_settings
from app.models.user import UserCreate, UserRole, UserStatus
import bcrypt

settings = get_settings()


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
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
        
        existing = await self.db.users.find_one({"email": user_data.email})
        if existing:
            raise ValueError("Email already registered")

       
        user_count = await self.db.users.count_documents({})
        role = UserRole.ADMIN if user_count == 0 else UserRole.VIEWER 

        
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
        user = await self.db.users.find_one({"email": email})
        if not user:
            raise ValueError("Invalid email or password")

        
        if not verify_password(password, user["password"]):
            raise ValueError("Invalid email or password")

        
        if user["status"] != UserStatus.ACTIVE:
            raise ValueError("Account is inactive, contact admin")

        
        token = create_access_token({
            "user_id": str(user["_id"]),
            "role": user["role"]
        })

        return {
            "access_token": token,
            "user": {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "status": user["status"]
            }
        }