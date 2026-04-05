from fastapi import APIRouter, Depends
from app.utils.response import success_response, failure_response
from app.services.dashboard_service import DashboardService
from app.middleware.auth_middleware import require_viewer, require_analyst
from app.database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


# ─── Summary (Sabhi roles) ───────────────────────────
@router.get("/summary")
async def get_summary(current_user: dict = Depends(require_viewer)):
    db = get_db()
    dashboard_service = DashboardService(db)

    try:
        summary = await dashboard_service.get_summary()
        return success_response(
            message="Summary fetched successfully",
            data=summary
        )
    except Exception as e:
        return failure_response(message="Something went wrong")


# ─── Category Breakdown (Analyst + Admin) ────────────
@router.get("/category-breakdown")
async def get_category_breakdown(current_user: dict = Depends(require_analyst)):
    db = get_db()
    dashboard_service = DashboardService(db)

    try:
        breakdown = await dashboard_service.get_category_breakdown()
        return success_response(
            message="Category breakdown fetched successfully",
            data=breakdown
        )
    except Exception as e:
        return failure_response(message="Something went wrong")


# ─── Monthly Trends (Analyst + Admin) ────────────────
@router.get("/monthly-trends")
async def get_monthly_trends(current_user: dict = Depends(require_analyst)):
    db = get_db()
    dashboard_service = DashboardService(db)

    try:
        trends = await dashboard_service.get_monthly_trends()
        return success_response(
            message="Monthly trends fetched successfully",
            data=trends
        )
    except Exception as e:
        return failure_response(message="Something went wrong")


# ─── Recent Activity (Sabhi roles) ───────────────────
@router.get("/recent-activity")
async def get_recent_activity(current_user: dict = Depends(require_viewer)):
    db = get_db()
    dashboard_service = DashboardService(db)

    try:
        activity = await dashboard_service.get_recent_activity()
        return success_response(
            message="Recent activity fetched successfully",
            data=activity
        )
    except Exception as e:
        return failure_response(message="Something went wrong")