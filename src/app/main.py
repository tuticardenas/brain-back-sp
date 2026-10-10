from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.routes.users import users_router

app = FastAPI(
    title="Brain Tutorship API",
    description="Backend API for Brain Tutorship",
    version="0.1.0"
)

# -----------------------------------------
# CORS
# -----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:9000",
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# -----------------------------------------
# Health Check
# -----------------------------------------
@app.get("/health", tags=["Health"], summary="Health Check")
async def health_check():
    return {"status":"ok"}

# -----------------------------------------
# Database conecction Check
# -----------------------------------------
@app.get("/db-check", tags=["Health"], summary="Check database")
async def check_database(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"database connected": result.scalar_one() == 1}


# -----------------------------------------
# Router registration
# -----------------------------------------
app.include_router(users_router)