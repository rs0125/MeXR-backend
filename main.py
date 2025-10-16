"""
MeXR Backend - Main Application Entry Point
A FastAPI backend for VR medical training simulation using LangChain and OpenAI.
"""

from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="MeXR Backend API",
    description="API endpoint to process queries for a VR medical simulation using LangChain and OpenAI.",
    version="1.0.0"
)

# Include API routes
app.include_router(router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "MeXR Backend is running",
        "documentation": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
