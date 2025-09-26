from sqlalchemy.orm import Session
from ...models import Vulnerability
from .kev import get_kev_set
from .epss import get_epss_map
from .nvd_seed import SAMPLE_NVD

async def refresh_vulns(db: Session):
    kev = await get_kev_set()
    epss = await get_epss_map()
    for cve, meta in SAMPLE_NVD.items():  # replace with real NVD later
        v = db.get(Vulnerability, cve) or Vulnerability(id=cve)
        v.title = meta["title"]
        v.cvss_base = meta.get("cvss", 0.0)
        v.epss = epss.get(cve, 0.0)
        v.known_exploited = cve in kev
        v.refs = meta.get("refs", {})
        db.add(v)
    db.commit()
