from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# ─── Record Type ─────────────────────────────────────
class RecordType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


# ─── Categories ──────────────────────────────────────
class RecordCategory(str, Enum):
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    SHOPPING = "shopping"
    OTHER = "other"


# ─── Create Record ───────────────────────────────────
class RecordCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    type: RecordType
    category: RecordCategory
    date: datetime
    notes: Optional[str] = Field(None, max_length=500)


# ─── Update Record ───────────────────────────────────
class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[RecordCategory] = None
    date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)


# ─── Record Response ─────────────────────────────────
class RecordResponse(BaseModel):
    id: str
    amount: float
    type: RecordType
    category: RecordCategory
    date: datetime
    notes: Optional[str] = None
    is_deleted: bool = False
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── Filter Params ───────────────────────────────────
class RecordFilter(BaseModel):
    type: Optional[RecordType] = None
    category: Optional[RecordCategory] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)