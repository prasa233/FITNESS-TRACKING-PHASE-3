

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from app.core.database import Base, engine
from app.routers import integrations
from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.models.user import User
from app.models import phase3
from fastapi import FastAPI
from app.routers.google_fit import router as google_fit_router

app = FastAPI()
app.include_router(google_fit_router)
# Import all Phase 3 routers.
from app.routers import (
    auth,
    nutrition,
    water,
    recommendations,
    timer,
    integrations,
    analytics,
    reminders,
)

# Create FastAPI application.
app = FastAPI(
    title="FitTrack Phase 3 API",
    description=(
        "FitTrack Phase 3 - Smart Features, "
        "External Integrations and Advanced Analytics"
    ),
    version="3.0.0",
)

# Allow the local Vite frontend to call this API from either hostname.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the authentication columns when upgrading the earlier ID-only users table.
# This keeps existing SQLite data and lets create_all() add its unique email index.
if engine.dialect.name == "sqlite" and inspect(engine).has_table("users"):
    with engine.begin() as connection:
        user_columns = {
            column["name"]
            for column in inspect(connection).get_columns("users")
        }
        if "email" not in user_columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR(255)"))
        if "password_hash" not in user_columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))

# Create database tables after all model modules are imported.
Base.metadata.create_all(bind=engine)


# Register Authentication.
app.include_router(auth.router)

# Register Nutrition.
app.include_router(nutrition.router)

# Register Water Tracking.
app.include_router(water.router)

# Register Workout Recommendations.
app.include_router(recommendations.router)

# Register Workout Timer.
app.include_router(timer.router)

# Register Fitness Integrations.
app.include_router(integrations.router)

# Register Advanced Analytics.
app.include_router(analytics.router)

# Register Reminders and Alerts.
app.include_router(reminders.router)


# Root endpoint.
@app.get("/", tags=["Home"])
def home():
    return {
        "message": "FitTrack Phase 3 Backend Running",
        "version": "3.0.0",
        "status": "SUCCESS",
        "modules": [
            "Nutrition",
            "Water Tracking",
            "Recommendations",
            "Workout Timer",
            "Integrations",
            "Analytics",
            "Reminders",
        ],
        "documentation": "/docs",
    }


# Health-check endpoint.
@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "application": "FitTrack Phase 3",
        "version": "3.0.0",
    }


# API module status endpoint.
@app.get("/api-status", tags=["Health"])
def api_status():
    return {
        "phase": 3,
        "status": "SUCCESS",
        "modules": {
            "nutrition": "IMPLEMENTED",
            "water_tracking": "IMPLEMENTED",
            "recommendations": "BASIC ENGINE",
            "workout_timer": "IMPLEMENTED",
            "integrations": "PREPARATION ONLY",
            "analytics": "PARTIAL",
            "reminders": "CRUD IMPLEMENTED",
        }
    }
class GoogleFitConnectRequest(BaseModel):
    # Replace this with the fields your endpoint actually requires.
    access_token: str = Field(min_length=1)


@app.post("/phase3/integrations/GOOGLE_FIT/connect")
async def connect_google_fit(request: GoogleFitConnectRequest):
    return {
        "status": "connected",
        "provider": "GOOGLE_FIT",
    }

