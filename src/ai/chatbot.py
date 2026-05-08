from pydantic_ai import Agent
from .shared import get_model
from ..database import get_db

agent = Agent(
    get_model(),
    system_prompt=(
        "You are a personal finance assistant. Answer questions about the user's expenses "
        "using the available tools. Be concise and specific. "
        "Format currency as $X.XX. "
        "Today's date is passed in the user message when relevant."
    ),
)


@agent.tool_plain
def get_expenses(
    category: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> list[dict]:
    """Retrieve expenses with optional filters. Dates use ISO 8601 format (YYYY-MM-DD)."""
    with get_db() as conn:
        query = "SELECT id, amount, date, description, category, merchant FROM expenses WHERE 1=1"
        params: list = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if from_date:
            query += " AND date >= ?"
            params.append(from_date)
        if to_date:
            query += " AND date <= ?"
            params.append(to_date)
        query += " ORDER BY date DESC"
        return [dict(r) for r in conn.execute(query, params).fetchall()]


@agent.tool_plain
def get_summary() -> dict:
    """Get total spending by category and monthly totals."""
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
            "by_category": [dict(r) for r in by_category],
            "monthly":     [dict(r) for r in monthly],
        }
