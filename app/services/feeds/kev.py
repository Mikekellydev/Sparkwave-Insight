import csv, httpx
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv"

async def get_kev_set() -> set[str]:
    s = set()
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get(KEV_URL)
        r.raise_for_status()
        for row in csv.DictReader(r.text.splitlines()):
            s.add(row.get("cveID","").strip())
    return s
