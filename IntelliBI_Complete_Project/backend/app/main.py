from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import init_db
from app.routes.dataset import router as dataset_router

app = FastAPI(
    title="IntelliBI - Multi-Agent Business Intelligence System",
    description="Upload business datasets and generate AI-assisted business insights.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"success": True, "message": "IntelliBI backend is running."}

app.include_router(dataset_router)
