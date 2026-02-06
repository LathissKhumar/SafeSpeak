from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import router
from app.core.logging import logger

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="SafeSpeak API - AI Guardian"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "online", "version": settings.VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=True)
