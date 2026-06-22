from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.database.connection import engine, Base

# API Routers Import
from app.api.auth import router as auth_router
from app.api.project import router as project_router
from app.api.task import router as task_router

# Model mapping for SQLAlchemy
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

# Physically create tables in PostgreSQL if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

# CORS configuration to allow your local frontend and online frontend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://taskflow-frontend-production-d2cd.up.railway.app", # ADICIONE ESTA LINHA
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers (including Authorization for the Token)
)

@app.exception_handler(SQLAlchemyError)
def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Captures any database error and sends a friendly response to the client.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal database communication error occurred. Please try again later."}
    )

# Include API routers
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "TaskFlow API running successfully! 🚀"}

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """Protected route that only responds if a valid JWT Token is provided."""
    return {
        "message": "You are authenticated!",
        "user_email": current_user.email,
        "user_id": current_user.id
    }