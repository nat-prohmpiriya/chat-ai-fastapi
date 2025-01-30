# schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # แปลง Beanie model เป็น Pydantic

class UpdateUserRequest(BaseModel):
    email: EmailStr | None = Field(
        None,
        description="New email address",
        example="newemail@example.com"
    )
    password: str | None = Field(
        None,
        min_length=8,
        description="New password (min 8 characters)",
        example="newpassword123"
    )