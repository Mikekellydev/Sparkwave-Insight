from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..services.feeds.refresh import refresh_vulns
import asyncio

router = APIRouter(prefix="/feeds", tags=["feeds"])

@router.post("/refresh")
async def refresh(db: Session = Depends(get_db)):
    await refresh_vulns(db)
    return {"status":"ok"}
