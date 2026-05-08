from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..models import Expense, ExpenseCreate, ExpenseUpdate, CATEGORIES
from ..database import get_db

router = APIRouter(prefix="/api")


@router.get("/expenses", response_model=list[Expense])
def list_expenses(
    category: Optional[str] = None,
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
):
    with get_db() as conn:
        query = "SELECT * FROM expenses WHERE 1=1"
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
        query += " ORDER BY date DESC, id DESC"
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


@router.post("/expenses", response_model=Expense, status_code=201)
def create_expense(expense: ExpenseCreate):
    if expense.category not in CATEGORIES:
        raise HTTPException(400, f"Category must be one of: {CATEGORIES}")
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO expenses (amount, date, description, category, merchant, notes, attachment_path) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (expense.amount, expense.date, expense.description,
             expense.category, expense.merchant, expense.notes, expense.attachment_path),
        )
        row = conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return dict(row)


@router.put("/expenses/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, expense: ExpenseUpdate):
    updates = {k: v for k, v in expense.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(400, "No fields to update")
    if "category" in updates and updates["category"] not in CATEGORIES:
        raise HTTPException(400, f"Category must be one of: {CATEGORIES}")
    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()
        if not existing:
            raise HTTPException(404, "Expense not found")
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        conn.execute(
            f"UPDATE expenses SET {set_clause} WHERE id = ?",
            (*updates.values(), expense_id),
        )
        row = conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()
        return dict(row)


@router.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    with get_db() as conn:
        result = conn.execute(
            "DELETE FROM expenses WHERE id = ?", (expense_id,)
        )
        if result.rowcount == 0:
            raise HTTPException(404, "Expense not found")


@router.get("/categories")
def get_categories():
    return CATEGORIES
