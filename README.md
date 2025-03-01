# pavement-identifier-backend
This project integrates a model that classifies pavement types based on input images. It supports both singular and batch processing, utilizing FastAPI for the backend and RabbitMQ for queuing and batch handling.

1. Install all packages:
pip install -r requirements.txt

2. Create a new folder called "secrets" in root drectory. A file called firebase-service-account.json would be dropped here

3. To startup the project:
Run "uvicorn main:app --reload" from root directory
