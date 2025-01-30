
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from src.models.user_model import User
from src.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Token validation error
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Check token type and user_id
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if not user_id or token_type != "access":
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Get user from DB
    user = await User.get(user_id)
    if not user or not user.is_active:
        raise credentials_exception
        
    return user