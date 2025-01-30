# services/user_service.py
from src.models.user_model import User
from src.utils.result import ok, err
from src.services.auth_service import AuthService

class UserService:
    def __init__(self):
        self.auth_service = AuthService()

    async def update_profile(
        self,
        user_id: str,
        email: str | None = None,
        password: str | None = None
    ):
        # 1. Get user
        user = await User.get(user_id)
        if not user:
            return err(404, "User not found")

        # 2. Update email
        if email and email != user.email:
            # Check email exists
            if await User.find_one(User.email == email):
                return err(400, "Email already exists")
            user.email = email

        # 3. Update password
        if password:
            user.hashed_password = self.auth_service.hash_password(password)

        # 4. Save
        await user.save()
        
        return ok({
            "id": str(user.id),
            "email": user.email,
            "is_active": user.is_active
        })