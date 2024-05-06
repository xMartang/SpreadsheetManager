from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from config import APP_NAME, DEBUG_MODE
from database import ensure_database_exists
from sheets.router import router as sheets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_database_exists()

    yield


app = FastAPI(title=APP_NAME, lifespan=lifespan, debug=DEBUG_MODE)
app.include_router(sheets_router)


@app.get("/")
async def root():
    """
    Redirect the user to the Swagger-UI documentation
    """
    return RedirectResponse(url="/docs/")
