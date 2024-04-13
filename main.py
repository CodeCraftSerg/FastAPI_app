# import uvicorn
import redis.asyncio as redis

from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes import contacts, auth, users
from src.conf.config import config

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# BASE_DIR = Path(".")
# app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")

BASE_DIR = Path(__file__).parent
directory = BASE_DIR.joinpath("src").joinpath("static")
app.mount("/static", StaticFiles(directory=directory), name="static")

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
    )
    await FastAPILimiter.init(r)


templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")  # noqa


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "our": "FastAPI application"}
    )


# @app.get("/")
# def index():
#     return {"message": "🔱 Contacts Application 🔱"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    Health Checker

    :param db: database session
    :return: health status
    :rtype: dict
    """
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
