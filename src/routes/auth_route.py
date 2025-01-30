# routes/auth_route.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse 
from src.services.auth_service import AuthService
from src.schemas.auth_schema import RegisterRequest, RefreshTokenRequest, TokenResponse
from src.utils.result import ok, err

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register",)  
async def register(data: RegisterRequest):
    result = await auth_service.register(data.email, data.password)
    if not result.ok:
        return JSONResponse(
            status_code=result.error.status,
            content={"message": result.error.message}
        )
    return JSONResponse(
        status_code=200,
        content=result.value
    )

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    result =  await auth_service.login(form_data.username, form_data.password)
    if not result.ok:
        return JSONResponse(
            status_code=result.error.status,
            content={"message": result.error.message}
        )
    return JSONResponse(
        status_code=200,
        content=result.value
    )

@router.post("/refresh",)
async def refresh_token(data: RefreshTokenRequest):
    result = await auth_service.refresh_token(data.refresh_token)
    if not result.ok:
        return JSONResponse(
            status_code=result.error.status,
            content={"message": result.error.message}
        )
    return JSONResponse(
        status_code=200,
        content=result.value
    )

