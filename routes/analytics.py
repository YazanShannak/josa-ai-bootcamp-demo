from fastapi import APIRouter
from database import get_db

router = APIRouter(prefix="/api/analytics")


@router.get("/summary")
def get_summary():
    with get_db() as conn:
        by_category = conn.execute(
            "SELECT category, ROUND(SUM(amount), 2) as total "
            "FROM expenses GROUP BY category ORDER BY total DESC"
        ).fetchall()
        monthly = conn.execute(
            "SELECT strftime('%Y-%m', date) as month, ROUND(SUM(amount), 2) as total "
            "FROM expenses GROUP BY month ORDER BY month DESC"
        ).fetchall()
        return {
            "by_category": [dict(row) for row in by_category],
            "monthly": [dict(row) for row in monthly],
        }
