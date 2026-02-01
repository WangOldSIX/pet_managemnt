"""
FastAPI Application Entry Point
Pet Management System Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import (
    business_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler,
    BusinessException
)
from sqlalchemy.exc import SQLAlchemyError
from app.api import api_router

# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    description="FastAPI + MySQL Pet Management System for Database Course",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global exception handlers
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Register API routes
app.include_router(api_router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Pet Management System API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print(f"""
    ========================================
    Pet Management System v{settings.APP_VERSION}
    ========================================
    Environment: {settings.ENVIRONMENT}
    API Docs: http://localhost:8000/docs
    Health: http://localhost:8000/health
    ========================================
    """)


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    print("Application shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
