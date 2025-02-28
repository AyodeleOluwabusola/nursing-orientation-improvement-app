from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.get("/config")
def get_config():
    return {
        "APP_NAME": settings.APP_NAME,
        "DEBUG": settings.DEBUG,
        "DATABASE_URL": settings.DATABASE_URL,
        "RABBITMQ_URL": settings.RABBITMQ_URL
    }





# # main.py
# import uvicorn
# from fastapi import FastAPI
# from app.database import engine
# from app.models.base import Base
# from app.routers import auth, matching, user
#
# def create_tables():
#     Base.metadata.create_all(bind=engine)
#
# app = FastAPI(title="Nursing Orientation Backend")
#
# @app.on_event("startup")
# def on_startup():
#     create_tables()
#
# # Include Routers
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(user.router, prefix="/api/users", tags=["users"])
# app.include_router(matching.router, prefix="/api/matching", tags=["matching"])
#
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
