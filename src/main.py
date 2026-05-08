from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import init_db
from .routes.analytics import router as analytics_router
from .routes.expenses import router as expenses_router
from .routes.chat import router as chat_router
from .routes.receipts import router as receipts_router

app = FastAPI(title="Othman Demo")

init_db()

app.include_router(expenses_router)
app.include_router(analytics_router)
app.include_router(chat_router)
app.include_router(receipts_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")
