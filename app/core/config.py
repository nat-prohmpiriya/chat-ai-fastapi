from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chat API"
    MONGODB_URL: str = "mongodb+srv://dackbok:bV9QsS6dJQo6p3Pb@cluster0.bi0ee.mongodb.net/chat_ai"
    
    class Config:
        env_file = ".env"

settings = Settings()