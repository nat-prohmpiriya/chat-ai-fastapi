
from beanie import Document, Indexed
from pydantic import EmailStr
from datetime import datetime
class User(Document):
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    is_active: bool = True
    deleted_at: datetime | None = None 

    class Settings:
        name = "users"
        timestamps = True  

    async def soft_delete(self):
        self.deleted_at = datetime.now()
        await self.save()

