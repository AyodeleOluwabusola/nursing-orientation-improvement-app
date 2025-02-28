from fastapi import FastAPI
from app.core.config import settings


app = FastAPI(title=settings.APP_NAME)

@app.get("/")
def home():
    return {"message": "Welcome to Pavement Identifier!"}


@app.get("/config")
def get_config():
    return {
        "APP_NAME": settings.APP_NAME,
        "DEBUG": settings.DEBUG,
        "DATABASE_URL": settings.DATABASE_URL,
        "RABBITMQ_URL": settings.RABBITMQ_URL
    }