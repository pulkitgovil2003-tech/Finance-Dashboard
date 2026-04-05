from datetime import datetime


class DashboardService:
    def __init__(self, db):
        self.db = db

    # ─── Summary ─────────────────────────────────────
    async def get_summary(self) -> dict:
        pipeline = [
            {"$match": {"is_deleted": False}},
            {
                "$group": {
                    "_id": "$type",
                    "total": {"$sum": "$amount"},
                    "count": {"$sum": 1}
                }
            }
        ]

        results = await self.db.records.aggregate(pipeline).to_list(length=10)

        total_income = 0.0
        total_expenses = 0.0
        total_records = 0

        for r in results:
            if r["_id"] == "income":
                total_income = r["total"]
                total_records += r["count"]
            elif r["_id"] == "expense":
                total_expenses = r["total"]
                total_records += r["count"]

        return {
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "net_balance": round(total_income - total_expenses, 2),
            "total_records": total_records
        }

    # ─── Category Breakdown ──────────────────────────
    async def get_category_breakdown(self) -> list:
        pipeline = [
            {"$match": {"is_deleted": False}},
            {
                "$group": {
                    "_id": "$category",
                    "total": {"$sum": "$amount"},
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"total": -1}}
        ]

        results = await self.db.records.aggregate(pipeline).to_list(length=50)

        return [
            {
                "category": r["_id"],
                "total": round(r["total"], 2),
                "count": r["count"]
            }
            for r in results
        ]

    # ─── Monthly Trends ──────────────────────────────
    async def get_monthly_trends(self) -> list:
        pipeline = [
            {"$match": {"is_deleted": False}},
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$date"},
                        "month": {"$month": "$date"},
                        "type": "$type"
                    },
                    "total": {"$sum": "$amount"}
                }
            },
            {"$sort": {"_id.year": -1, "_id.month": -1}}
        ]

        results = await self.db.records.aggregate(pipeline).to_list(length=100)

        # Data organize karo month wise
        months = {}
        for r in results:
            year = r["_id"]["year"]
            month = r["_id"]["month"]
            type_ = r["_id"]["type"]
            key = f"{year}-{str(month).zfill(2)}"

            if key not in months:
                months[key] = {
                    "month": key,
                    "total_income": 0.0,
                    "total_expenses": 0.0,
                    "net": 0.0
                }

            if type_ == "income":
                months[key]["total_income"] = round(r["total"], 2)
            elif type_ == "expense":
                months[key]["total_expenses"] = round(r["total"], 2)

        # Net calculate karo
        trends = []
        for key in sorted(months.keys(), reverse=True):
            m = months[key]
            m["net"] = round(m["total_income"] - m["total_expenses"], 2)
            trends.append(m)

        return trends

    # ─── Recent Activity ─────────────────────────────
    async def get_recent_activity(self) -> list:
        records = await self.db.records.find(
            {"is_deleted": False}
        ).sort("created_at", -1).limit(10).to_list(length=10)

        return [
            {
                "id": str(r["_id"]),
                "amount": r["amount"],
                "type": r["type"],
                "category": r["category"],
                "date": r["date"].strftime("%Y-%m-%d"),
                "notes": r.get("notes")
            }
            for r in records
        ]