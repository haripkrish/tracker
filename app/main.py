from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.api_v1.api import api_router
import logging
from app.db import init_db

logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing test data in db...")
    init_db.main()
    logger.info("Initializing test data Complete")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{'/api/v1'}/openapi.json",
    lifespan=lifespan,
)



@app.get("/")
def ping():
    return {"result": "pong"}


app.include_router(api_router, prefix='/api/v1')
