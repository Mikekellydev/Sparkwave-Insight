from sqlalchemy.orm import Session
from ...models import Vulnerability
from .kev import get_kev_set
from .epss import get_epss_map
from .nvd_seed import SAMPLE_NVD

async def refresh_vulns(db: Session):
    kev = set()
    epss = {}
    # Best-effort KEV
    try:
        kev = await get_kev_set()
    except Exception as e:
        print(f"[feeds] KEV fetch failed: {e}")
    # Best-effort EPSS
    try:
        epss = await get_epss_map()
    except Exception as e:
        print(f"[feeds] EPSS fetch failed: {e}")

    # Seed/refresh vulns from the sample set (replace with real NVD later)
    for cve, meta in SAMPLE_NVD.items():
        v = db.get(Vulnerability, cve) or Vulnerability(id=cve)
        v.title = meta.get("title")
        v.cvss_base = float(meta.get("cvss", 0.0) or 0.0)
        v.epss = float(epss.get(cve, 0.0) or 0.0)
        v.known_exploited = cve in kev
        v.refs = meta.get("refs", {})
        db.add(v)
    db.commit()
