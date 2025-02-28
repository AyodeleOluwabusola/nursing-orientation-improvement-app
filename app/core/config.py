from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Pavement Identifier"
    DEBUG: bool = False
    DATABASE_URL: str = '444'
    RABBITMQ_URL: str = '444'
    QUEUE_NAME: str = '333'
    RABBITMQ_HOST: str = '39876'

    class Config:
        env_file = ".env"

# Instantiate settings
settings = Settings()