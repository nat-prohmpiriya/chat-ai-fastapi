from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Chat API")

# API Router
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=5001, reload=True)