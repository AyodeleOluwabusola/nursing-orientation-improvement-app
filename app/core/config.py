from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Nursing Orientation Improvement"
    DEBUG: bool = False
    DATABASE_URL: str = ''
    RABBITMQ_URL: str = ''
    QUEUE_NAME: str
    RABBITMQ_HOST: str

    class Config:
        env_file = ".env"

# Instantiate settings
settings = Settings()