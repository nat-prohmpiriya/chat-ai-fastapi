# routes/user_route.py
from fastapi import APIRouter, Depends
from src.dependencies.auth_deps import get_current_user
from src.models.user_model import User
from src.services.user_service import UserService
from src.schemas.user_schema import UpdateUserRequest, UserResponse  
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()

@router.get("/me")
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_profile(
    data: UpdateUserRequest,
    current_user: User = Depends(get_current_user)
):
    result = await user_service.update_profile(
        user_id=str(current_user.id),
        email=data.email,
        password=data.password
    )
    if not result.ok:
        return JSONResponse(
            status_code=result.error.status,
            content={"message": result.error.message}
        )
    return JSONResponse(
        status_code=200,
        content=result.value
    )