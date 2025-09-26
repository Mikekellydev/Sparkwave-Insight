from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Asset, Vulnerability, Finding
from ..services.risk import score

router = APIRouter(prefix="/findings", tags=["findings"])

@router.post("/")
def create_finding(payload: dict, db: Session = Depends(get_db)):
    asset_id = payload.get("asset_id")
    cve_id   = payload.get("cve_id")
    severity = payload.get("severity","medium")
    if not (asset_id and cve_id):
        raise HTTPException(400, "asset_id and cve_id are required")

    a = db.get(Asset, asset_id); v = db.get(Vulnerability, cve_id)
    if not a: raise HTTPException(404, "asset not found")
    if not v: raise HTTPException(404, "vulnerability not found (run feed refresh)")

    f = Finding(asset_id=a.id, cve_id=v.id, severity=severity, evidence={})
    f.risk_score = score(cvss=v.cvss_base or 0, epss=v.epss or 0, kev=v.known_exploited, crit=a.business_criticality if hasattr(a,"business_criticality") else 1)
    db.add(f); db.commit(); db.refresh(f)
    return {
        "id": f.id, "asset_id": f.asset_id, "cve_id": f.cve_id,
        "severity": f.severity, "risk_score": f.risk_score
    }

@router.get("/")
def list_findings(db: Session = Depends(get_db)):
    return [
        {"id": x.id, "asset_id": x.asset_id, "cve_id": x.cve_id, "severity": x.severity, "risk_score": x.risk_score}
        for x in db.query(Finding).all()
    ]
