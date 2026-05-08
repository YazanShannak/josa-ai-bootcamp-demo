from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import init_db
from routes.expenses import router as expenses_router
from routes.analytics import router as analytics_router

app = FastAPI(title="Othman Demo")

init_db()

app.include_router(expenses_router)
app.include_router(analytics_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")
