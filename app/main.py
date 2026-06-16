from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app import models
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="URL Shortener", lifespan=lifespan)
app.include_router(router)