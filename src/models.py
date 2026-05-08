from pydantic import BaseModel, Field
from typing import Optional

CATEGORIES = ["Food", "Transport", "Housing", "Entertainment", "Health", "Other"]


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    date: str
    description: str
    category: str
    merchant: Optional[str] = None
    notes: Optional[str] = None
    attachment_path: Optional[str] = None


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    merchant: Optional[str] = None
    notes: Optional[str] = None


class Expense(BaseModel):
    id: int
    amount: float
    date: str
    description: str
    category: str
    merchant: Optional[str] = None
    notes: Optional[str] = None
    attachment_path: Optional[str] = None
    created_at: str
