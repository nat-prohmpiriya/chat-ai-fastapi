from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, User
from app.api import deps

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    return {"msg": "create user"}