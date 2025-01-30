import os
from dotenv import load_dotenv
from .settings import settings

load_dotenv()

class Environment:
    OPENAI_API_KEY = settings.OPENAI_API_KEY
    ANTHROPIC_API_KEY = settings.ANTHROPIC_API_KEY
    GEMINI_API_KEY = settings.GEMINI_API_KEY
