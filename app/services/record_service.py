from datetime import datetime
from bson import ObjectId
from app.models.record import RecordCreate, RecordUpdate, RecordFilter


class RecordService:
    def __init__(self, db):
        self.db = db

    def _format_record(self, record: dict) -> dict:
        return {
            "id": str(record["_id"]),
            "amount": record["amount"],
            "type": record["type"],
            "category": record["category"],
            "date": record["date"],
            "notes": record.get("notes"),
            "is_deleted": record.get("is_deleted", False),
            "created_by": str(record["created_by"]),
            "created_at": record["created_at"],
            "updated_at": record.get("updated_at")
        }

    # ─── Create Record ───────────────────────────────
    async def create_record(self, record_data: RecordCreate, user_id: str) -> dict:
        user = await self.db.users.find_one({"_id": ObjectId(user_id)})
        record_doc = {
            "amount": record_data.amount,
            "type": record_data.type,
            "category": record_data.category,
            "date": record_data.date,
            "notes": record_data.notes,
            "is_deleted": False,
            "created_by": user["email"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = await self.db.records.insert_one(record_doc)
        record_doc["_id"] = result.inserted_id
        return self._format_record(record_doc)

    # ─── Get All Records with Filters ────────────────
    async def get_records(self, filters: RecordFilter) -> dict:
        query = {"is_deleted": False}

        # Filters apply karo
        if filters.type:
            query["type"] = filters.type
        if filters.category:
            query["category"] = filters.category
        if filters.from_date or filters.to_date:
            query["date"] = {}
            if filters.from_date:
                query["date"]["$gte"] = filters.from_date
            if filters.to_date:
                query["date"]["$lte"] = filters.to_date

        skip = (filters.page - 1) * filters.limit
        total = await self.db.records.count_documents(query)

        records = await self.db.records.find(query)\
            .sort("date", -1)\
            .skip(skip)\
            .limit(filters.limit)\
            .to_list(length=filters.limit)

        return {
            "records": [self._format_record(r) for r in records],
            "total": total,
            "page": filters.page,
            "limit": filters.limit,
            "total_pages": (total + filters.limit - 1) // filters.limit
        }

    # ─── Get Single Record ───────────────────────────
    async def get_record_by_id(self, record_id: str) -> dict:
        if not ObjectId.is_valid(record_id):
            raise ValueError("Invalid record ID")

        record = await self.db.records.find_one({
            "_id": ObjectId(record_id),
            "is_deleted": False
        })

        if not record:
            raise ValueError("Record not found")

        return self._format_record(record)

    # ─── Update Record ───────────────────────────────
    async def update_record(self, record_id: str, update_data: RecordUpdate) -> dict:
        if not ObjectId.is_valid(record_id):
            raise ValueError("Invalid record ID")

        update_fields = {
            k: v for k, v in update_data.model_dump(exclude_unset=True).items()
        }

        if not update_fields:
            raise ValueError("No fields to update")

        update_fields["updated_at"] = datetime.utcnow()

        result = await self.db.records.update_one(
            {"_id": ObjectId(record_id), "is_deleted": False},
            {"$set": update_fields}
        )

        if result.matched_count == 0:
            raise ValueError("Record not found")

        return await self.get_record_by_id(record_id)


    # ─── Soft Delete ─────────────────────────────────
    async def delete_record(self, record_id: str) -> bool:
        if not ObjectId.is_valid(record_id):
            raise ValueError("Invalid record ID")

        result = await self.db.records.update_one(
            {"_id": ObjectId(record_id), "is_deleted": False},
            {"$set": {
                "is_deleted": True,
                "updated_at": datetime.utcnow()
            }}
        )

        if result.matched_count == 0:
            raise ValueError("Record not found")

        return True