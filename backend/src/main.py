from fastapi import FastAPI
from starlette.responses import RedirectResponse

from config import APP_NAME
from database import ensure_database_exists
from sheets.router import router as sheets_router

app = FastAPI(title=APP_NAME)
app.include_router(sheets_router)


@app.on_event("startup")
async def on_startup():
    ensure_database_exists()


@app.get("/")
async def root():
    """
    Redirect the user to the Swagger-UI documentation
    """
    return RedirectResponse(url="/docs/")
