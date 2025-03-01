from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Nursing Orientation Improvement"
    DEBUG: bool = False
    DATABASE_URL: str = '444'
    RABBITMQ_URL: str = '444'
    QUEUE_NAME: str = '333'
    RABBITMQ_HOST: str = '39876'
    ADD_MENTOR: str = 'http://127.0.0.1:7000/embedmentor'
    MATCH_URL: str = 'http://127.0.0.1:7000/returnmentors'

    class Config:
        env_file = ".env"

# Instantiate settings
settings = Settings()