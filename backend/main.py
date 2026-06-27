from fastapi import FastAPI
from backend.app.Schema.user import User, UserPreference, UserProfile
from backend.app.routes.auth_routes import router as auth_router
from backend.app.routes.alert_route import router as alert_router
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.connection import init_db

app = FastAPI(
    title="Weather Alert System API",
    description="Weather Forecast and Alert Background",
    version="1.0"
)
# CORS Configuration
app.add_middleware(

    CORSMiddleware,

   allow_origins=[
    "http://localhost:3000",
    "http://localhost:5173",
],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


init_db()
app.include_router(auth_router)
app.include_router(alert_router)

@app.get("/")
def home():
    return {
        "message": "Weather Alert API Running"
    }





