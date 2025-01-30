from fastapi import FastAPI
from internal.auth.handler import auth_router
import uvicorn
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

app = FastAPI(title="Chat API")

# Routes
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "server is up and running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)