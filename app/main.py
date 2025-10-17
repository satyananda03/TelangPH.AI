from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.predict import predict_routes

app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware,
                    allow_origins=origins,             # Domain yang diizinkan
                    allow_credentials=True,            # Mengizinkan cookie/header otorisasi
                    allow_methods=["*"],               # Mengizinkan semua metode HTTP (GET, POST, PUT, dll.)
                    allow_headers=["*"])
                    
app.include_router(predict_routes)
# uvicorn run:app --reload --host 0.0.0.0 --port 8000