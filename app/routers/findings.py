from fastapi import APIRouter
router = APIRouter(prefix="/findings", tags=["findings"])
@router.get("/")
def list_findings():
    return []
