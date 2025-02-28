import uvicorn
from fastapi import FastAPI
from app.firebase_app import firebase_app
from app.routers import auth, data
from app.core.config import settings

app = FastAPI(title="Nursing Orientation ImproFvement Backend")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
