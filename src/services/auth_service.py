# services/auth_service.py
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError

from src.models.user_model import User
from src.config.settings import settings
from src.utils.result import ok, err, Result

pwd_context = CryptContext(schemes=["bcrypt"])

class AuthService:
    async def register(self, email: str, password: str) -> Result:
        if await User.find_one(User.email == email):
            return err(400, "Email already exists")
        
        user = User(
            email=email,
            hashed_password=self._hash_password(password) 
        )
        await user.create()
        
        access_token = self._create_access_token({"sub": str(user.id)})
        refresh_token = self._create_refresh_token({"sub": str(user.id)})
        
        return ok({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        })
    
    async def login(self, email: str, password: str):
        # Find user
        user = await User.find_one(User.email == email)
        if not user:
            return err(401, "Invalid credentials")
            
        # Verify password
        if not self._verify_password(password, user.hashed_password):
            return err(401, "Invalid credentials")
            
        # Create tokens
        return ok({
            "access_token": self._create_access_token(str(user.id)),
            "refresh_token": self._create_refresh_token(str(user.id))
        })

    async def refresh_token(self, refresh_token: str):
        try:
            # 1. Verify refresh token
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            # 2. Check token type
            if payload.get("type") != "refresh":
                return err(401, "Invalid token type")
                
            # 3. Get user_id
            user_id = payload.get("sub")
            if not user_id:
                return err(401, "Invalid token")
                
            # 4. Check user exists
            user = await User.get(user_id)
            if not user or not user.is_active:
                return err(401, "User not found or inactive")
                
            # 5. Create new tokens
            return ok({
                "access_token": self._create_access_token(user_id),
                "refresh_token": self._create_refresh_token(user_id)
            })
            
        except JWTError:
            return err(401, "Invalid or expired token")

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def _verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def _create_access_token(self, user_id: str) -> str:
        expires = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self._create_token({"sub": user_id, "type": "access"}, expires)

    def _create_refresh_token(self, user_id: str) -> str:
        expires = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        return self._create_token({"sub": user_id, "type": "refresh"}, expires)

    def _create_token(self, data: dict, expires: datetime) -> str:
        data.update({"exp": expires})
        return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)