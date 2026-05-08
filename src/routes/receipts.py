import io
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, UploadFile
from openai import AsyncOpenAI

from ..ai.receipt_agent import extract_from_image, extract_from_text

load_dotenv()

router = APIRouter(prefix="/api")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

SUPPORTED_IMAGE = {"image/jpeg", "image/png", "image/webp", "image/gif"}
SUPPORTED_AUDIO = {"audio/mpeg", "audio/mp4", "audio/wav", "audio/webm", "audio/ogg"}


async def _transcribe(file_bytes: bytes, filename: str) -> str:
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    audio = io.BytesIO(file_bytes)
    audio.name = filename
    transcript = await client.audio.transcriptions.create(
        model="whisper-1",
        file=audio,
    )
    return transcript.text


@router.post("/parse-receipt")
async def parse_receipt(file: UploadFile):
    content_type = file.content_type or ""
    file_bytes = await file.read()

    if content_type in SUPPORTED_IMAGE:
        extraction = await extract_from_image(file_bytes, content_type)
    elif content_type in SUPPORTED_AUDIO:
        transcript = await _transcribe(file_bytes, file.filename or "audio.mp3")
        extraction = await extract_from_text(transcript)
    else:
        raise HTTPException(
            400,
            f"Unsupported file type '{content_type}'. Upload a receipt image or audio file."
        )

    ext = Path(file.filename or "file").suffix or ".bin"
    saved_name = f"{uuid.uuid4()}{ext}"
    (UPLOAD_DIR / saved_name).write_bytes(file_bytes)

    return {**extraction.model_dump(), "attachment_path": f"uploads/{saved_name}"}
