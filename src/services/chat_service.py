from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
import google.generativeai as genai
from ..config.settings import settings

class ChatService:
    def __init__(self):
        self.settings = settings
        self.models = {
            "openai": self._init_openai,
            "anthropic": self._init_anthropic,
            "gemini": self._init_gemini
        }
        
    def _init_openai(self, config: Dict[str, Any]):
        return ChatOpenAI(
            openai_api_key=self.settings.OPENAI_API_KEY,
            model_name=config.get("model", "gpt-3.5-turbo"),
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 1000)
        )
    
    def _init_anthropic(self, config: Dict[str, Any]):
        return ChatAnthropic(
            anthropic_api_key=self.settings.ANTHROPIC_API_KEY,
            model_name=config.get("model", "claude-2"),
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 1000)
        )
    
    def _init_gemini(self, config: Dict[str, Any]):
        genai.configure(api_key=self.settings.GEMINI_API_KEY)
        generation_config = {
            "temperature": config.get("temperature", 0.7),
            "max_output_tokens": config.get("max_tokens", 1000),
        }
        model = genai.GenerativeModel(
            model_name=config.get("model", "gemini-pro"),
            generation_config=generation_config
        )
        return model
    
    async def chat(self, provider: str, message: str, config: Dict[str, Any]) -> str:
        try:
            if provider not in self.models:
                raise ValueError(f"Provider {provider} not supported")
                
            model = self.models[provider](config)
            
            if provider == "gemini":
                response = model.generate_content(message)
                return response.text
                
            messages = [
                SystemMessage(content=config.get("system_message", "You are a helpful assistant.")),
                HumanMessage(content=message)
            ]
            
            response = model.invoke(messages)
            return response.content
            
        except Exception as e:
            print(f"Error in chat service: {str(e)}")
            raise e
