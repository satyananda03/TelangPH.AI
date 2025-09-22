from fastapi import FastAPI
from app.endpoints.predict import predict_routes

app = FastAPI()

app.include_router(predict_routes)
# uvicorn run:app --reload --host 0.0.0.0 --port 8000