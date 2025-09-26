import csv, httpx
EPSS_URL = "https://epss.cyentia.com/epss_scores-current.csv.gz"

async def get_epss_map() -> dict[str,float]:
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get(EPSS_URL)
        r.raise_for_status()
        import gzip, io
        z = gzip.GzipFile(fileobj=io.BytesIO(r.content))
        m = {}
        for row in csv.DictReader(io.TextIOWrapper(z, encoding="utf-8")):
            m[row["cve"]] = float(row["epss"])
        return m
