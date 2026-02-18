"""
AIaaS Finance Platform - Main Application
==========================================
Entry point for the FastAPI application
Runs both FastAPI (port 8000) and Flask WebSocket server (port 5000)
"""

import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.ai_calling.views_actual import router as ai_calling_router
from app.data_ingestion.views import router as data_ingestion_router
from app.ai_calling.views import router as ai_calling_router
from app.auth.views import router as auth_router

app = FastAPI(
    title="AIaaS Finance Platform",
    version="1.0.0",
    description="AI as a Service for Finance Agencies"
)

# --- CORS (allow all for development; restrict in production) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (expand as phases progress)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(ai_calling_router, prefix="/ai_calling", tags=["AI Calling"])
app.include_router(data_ingestion_router, prefix="/data_ingestion", tags=["Data Ingestion"])


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AIaaS Finance Platform API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "data_ingestion": "/data_ingestion",
            "ai_calling": "/ai_calling",
            "health": "/ai_calling/health",
            "flask_webhooks": "http://localhost:5000/webhooks/*",
            "flask_websocket": "ws://localhost:5000/socket/<uuid>"
        },
        "servers": {
            "fastapi": "http://127.0.0.1:8000 (API endpoints)",
            "flask": "http://127.0.0.1:5000 (Webhooks & WebSocket)"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """General health check endpoint"""
    return {
        "status": "healthy",
        "service": "AIaaS Finance Platform",
        "fastapi_port": 8000,
        "flask_port": 5000
    }


    # Start FastAPI server
    # Render provides PORT env var, otherwise default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)