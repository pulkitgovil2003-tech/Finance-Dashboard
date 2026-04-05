from fastapi import APIRouter, Depends
from app.utils.response import success_response, failure_response
from app.models.record import RecordCreate, RecordUpdate, RecordFilter, RecordType, RecordCategory
from app.services.record_service import RecordService
from app.middleware.auth_middleware import require_admin, require_analyst
from app.database import get_db
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/records", tags=["Records"])


# ─── Create Record (Admin only) ──────────────────────
@router.post("/")
async def create_record(
    record_data: RecordCreate,
    current_user: dict = Depends(require_admin)
):
    db = get_db()
    record_service = RecordService(db)

    try:
        record = await record_service.create_record(
            record_data,
            str(current_user["_id"])
        )
        return success_response(
            message="Record created successfully",
            data=record
        )
    except ValueError as e:
        return failure_response(message=str(e))
    except Exception as e:
        return failure_response(message="Something went wrong")


# ─── Get All Records (Analyst + Admin) ───────────────
@router.get("/")
async def get_records(
    type: Optional[RecordType] = None,
    category: Optional[RecordCategory] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    page: int = 1,
    limit: int = 10,
    current_user: dict = Depends(require_analyst)
):
    db = get_db()
    record_service = RecordService(db)

    try:
        filters = RecordFilter(
            type=type,
            category=category,
            from_date=from_date,
            to_date=to_date,
            page=page,
            limit=limit
        )
        records = await record_service.get_records(filters)
        return success_response(
            message="Records fetched successfully",
            data=records
        )
    except ValueError as e:
        return failure_response(message=str(e))
    except Exception as e:
        return failure_response(message="Something went wrong")


# ─── Get Single Record (Analyst + Admin) ─────────────
@router.get("/{record_id}")
async def get_record(
    record_id: str,
    current_user: dict = Depends(require_analyst)
):
    db = get_db()
    record_service = RecordService(db)

    try:
        record = await record_service.get_record_by_id(record_id)
        return success_response(
            message="Record fetched successfully",
            data=record
        )
    except ValueError as e:
        return failure_response(message=str(e))
    except Exception as e:
        return failure_response(message="Something went wrong")


# ─── Update Record (Admin only) ──────────────────────
@router.patch("/{record_id}")
async def update_record(
    record_id: str,
    update_data: RecordUpdate,
    current_user: dict = Depends(require_admin)
):
    db = get_db()
    record_service = RecordService(db)

    try:
        record = await record_service.update_record(record_id, update_data)
        return success_response(
            message="Record updated successfully",
            data=record
        )
    except ValueError as e:
        return failure_response(message=str(e))
    except Exception as e:
        return failure_response(message="Something went wrong")


# ─── Delete Record (Admin only) ──────────────────────
@router.delete("/{record_id}")
async def delete_record(
    record_id: str,
    current_user: dict = Depends(require_admin)
):
    db = get_db()
    record_service = RecordService(db)

    try:
        await record_service.delete_record(record_id)
        return success_response(message="Record deleted successfully")
    except ValueError as e:
        return failure_response(message=str(e))
    except Exception as e:
        return failure_response(message="Something went wrong")
    