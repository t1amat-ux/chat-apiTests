from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.database import engine, Base
from app.routers import chats
from app.config import settings


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting application...")
    Base.metadata.create_all(bind=engine)
    yield

    logger.info("Shutting down application...")

app = FastAPI(
    title="Chat API",
    description="API for managing chats and messages",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(chats.router, prefix="/api", tags=["chats"])

@app.get("/")
async def root():
    return {"message": "Chat API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}