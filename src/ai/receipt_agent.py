from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent

from .shared import get_model

CATEGORIES = ["Food", "Transport", "Housing", "Entertainment", "Health", "Other"]


class ExpenseExtraction(BaseModel):
    amount: float
    date: str           # ISO 8601 (YYYY-MM-DD)
    description: str
    category: str       # must be one of CATEGORIES
    merchant: str | None = None


_agent = Agent(
    get_model(),
    output_type=ExpenseExtraction,
    system_prompt=(
        f"Extract expense details from the provided receipt image or text transcript. "
        f"category MUST be one of: {', '.join(CATEGORIES)}. "
        f"date MUST be ISO 8601 (YYYY-MM-DD) — use today's date if not visible. "
        f"amount must be a positive number. "
        f"description should be a short, clear label for the expense."
    ),
)


async def extract_from_image(image_bytes: bytes, content_type: str) -> ExpenseExtraction:
    result = await _agent.run(
        [BinaryContent(data=image_bytes, media_type=content_type)]
    )
    return result.output


async def extract_from_text(transcript: str) -> ExpenseExtraction:
    result = await _agent.run(f"Voice memo transcript: {transcript}")
    return result.output
