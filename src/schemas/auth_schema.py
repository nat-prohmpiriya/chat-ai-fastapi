# schemas/auth.py
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class RegisterRequest(BaseModel):
    email: EmailStr = Field(
        ...,  # required
        description="Valid email address",
        example="user@example.com"
    )

    password: str = Field(
        ...,  # required
        min_length=8,
        description="Password must be at least 8 characters long",
        example="strongpassword123"
    )

class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Your email address",
        example="user@example.com"
    )
    password: str = Field(
        ...,
        description="Your password",
        example="password123"
    )

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        ...,
        description="Refresh token",
        example="eyJhbGciOiJIUzI1NiIs..."
    )

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"  # ค่าคงที่

class RefreshTokenRequest(BaseModel):
    refresh_token: str
