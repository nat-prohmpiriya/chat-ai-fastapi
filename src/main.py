# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.config.settings import settings
from src.models.user_model import User
from src.routes import auth_route, user_route

# 1. Create FastAPI app
app = FastAPI(
    title="User Auth API",
    description="FastAPI User Authentication System",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc UI
    openapi_url="/openapi.json"
)

# Add middleware

# 2. Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ในโปรดักชันควรระบุ domain ที่อนุญาต
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Database initialization
@app.on_event("startup")
async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[User]  # เพิ่ม models ที่นี่
    )

# 4. Add routes
app.include_router(auth_route.router)
app.include_router(user_route.router)

# 5. Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}