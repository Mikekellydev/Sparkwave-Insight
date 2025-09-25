# app/routers/assets.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Asset

router = APIRouter(prefix="/assets", tags=["assets"])

@router.post("/")
def create_asset(payload: dict, db: Session = Depends(get_db)):
    a = Asset(hostname=payload.get("hostname", "unnamed"))
    db.add(a); db.commit(); db.refresh(a)
    return {"id": a.id, "hostname": a.hostname}

@router.get("/")
def list_assets(db: Session = Depends(get_db)):
    return [{"id": a.id, "hostname": a.hostname} for a in db.query(Asset).all()]
