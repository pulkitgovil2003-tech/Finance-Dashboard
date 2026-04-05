from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


# ─── Roles ───────────────────────────────────────────
class UserRole(str, Enum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"


# ─── User Status ─────────────────────────────────────
class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# ─── Create User (Register) ──────────────────────────
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


# ─── Update User ─────────────────────────────────────
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None


# ─── Update Role (Admin only) ────────────────────────
class UserRoleUpdate(BaseModel):
    role: UserRole


# ─── Update Status (Admin only) ──────────────────────
class UserStatusUpdate(BaseModel):
    status: UserStatus


# ─── User Response (password nahi bhejenge) ──────────
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    status: UserStatus
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Token Models ────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[UserRole] = None