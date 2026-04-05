from pydantic import BaseModel
from typing import List, Optional


# ─── Summary ─────────────────────────────────────────
class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    total_records: int


# ─── Category Breakdown ──────────────────────────────
class CategoryBreakdown(BaseModel):
    category: str
    total: float
    count: int


# ─── Monthly Trend ───────────────────────────────────
class MonthlyTrend(BaseModel):
    month: str        # "2024-01"
    total_income: float
    total_expenses: float
    net: float


# ─── Recent Activity ─────────────────────────────────
class RecentActivity(BaseModel):
    id: str
    amount: float
    type: str
    category: str
    date: str
    notes: Optional[str] = None


# ─── Dashboard Response Models ───────────────────────
class SummaryResponse(BaseModel):
    summary: DashboardSummary


class CategoryBreakdownResponse(BaseModel):
    breakdown: List[CategoryBreakdown]


class MonthlyTrendResponse(BaseModel):
    trends: List[MonthlyTrend]


class RecentActivityResponse(BaseModel):
    activities: List[RecentActivity]