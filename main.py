import uvicorn
from fastapi import FastAPI

from app.firebase_app import firebase_app
from app.routers import auth, data, user, match
from app.core.config import settings
from app.database import engine
from app.models.base import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Nursing Orientation Improvement Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_tables():
    Base.metadata.create_all(bind=engine)

def drop_tables():
    Base.metadata.drop_all(bind=engine)

@app.on_event("startup")
def on_startup():
    create_tables()
@app.get("/")
def read_root():
    return {"message": "Hello, Nursing Orientation Improvement!"}

@app.get("/config")
def get_config():
    return {
        "APP_NAME": settings.APP_NAME,
        "DEBUG": settings.DEBUG,
        "DATABASE_URL": settings.DATABASE_URL,
        "RABBITMQ_URL": settings.RABBITMQ_URL
    }
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(match.router, prefix="/api/match", tags=["match"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
