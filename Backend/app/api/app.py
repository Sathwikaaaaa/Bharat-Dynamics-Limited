from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.root import router as root_router
from app.api.routes.auth import router as auth_router
from app.api.routes.invoices import router as invoices_router

from app.queue.queue_manager import queue_service
from app.workers.invoice_worker import start_worker


worker = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global worker

    worker = start_worker(queue_service)

    yield

    if worker:
        worker.running = False


app = FastAPI(
    title="Bharat Dynamics Invoice OCR API",
    description="REST API for invoice OCR and information extraction",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(root_router)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(invoices_router)