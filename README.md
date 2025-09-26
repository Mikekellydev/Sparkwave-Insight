# Sparkwave-Insight

> Mission-first vulnerability management MVP — built with FastAPI, PostgreSQL, and Docker.

Sparkwave-Insight is an early prototype vulnerability management platform inspired by Rapid7 InsightVM.  
It demonstrates asset tracking, vulnerability ingestion, risk scoring, and reporting — all containerized for easy deployment.

---

## ✨ Features (MVP)

- **FastAPI + PostgreSQL** backend
- **Assets API** — register and query hosts
- **Findings API** — attach CVEs to assets with computed `risk_score`
- **Feeds API** — refresh sample vulnerabilities and merge KEV/EPSS data (best-effort, no crash on network errors)
- **Summary Report API** — aggregated view of assets, findings, severity, top-risk assets, KEV exposure
- **Swagger UI / ReDoc** — branded API docs at `/docs` and `/redoc`
- **Healthcheck** — quick status at `/health/`

---

## 🚀 Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- (Optional) `curl` or `httpie` for CLI testing

### Clone the repo
```bash
git clone https://github.com/your-org/sparkwave-insight.git
cd sparkwave-insight
Build & run with Docker Compose
bash
Copy code
# build and start services
sudo docker compose up -d --build

# check containers
sudo docker compose ps
API: http://127.0.0.1:8000

Docs: http://127.0.0.1:8000/docs

Health: http://127.0.0.1:8000/health/

🔎 Example Usage
1. Refresh vulnerability feeds
bash
Copy code
curl -X POST http://127.0.0.1:8000/feeds/refresh
2. Create an asset
bash
Copy code
curl -X POST http://127.0.0.1:8000/assets/ \
  -H 'Content-Type: application/json' \
  -d '{"hostname":"web-01","ip":"10.0.0.10","os_name":"Ubuntu","os_version":"22.04","business_criticality":4}'
3. Create a finding (auto-scored)
bash
Copy code
curl -X POST http://127.0.0.1:8000/findings/ \
  -H 'Content-Type: application/json' \
  -d '{"asset_id":1,"cve_id":"CVE-2024-12345","severity":"critical"}'
4. View findings
bash
Copy code
curl http://127.0.0.1:8000/findings/
5. Get summary report
bash
Copy code
curl http://127.0.0.1:8000/report/summary
Example response:

json
Copy code
{
  "assets": 2,
  "findings": 3,
  "severity": {"critical": 1, "high": 1, "medium": 1, "low": 0},
  "total_risk": 176.2,
  "kev_exposure": 1,
  "top_assets_by_risk": [
    {"asset_id": 1, "hostname": "web-01", "total_risk": 120.0}
  ]
}
🛠️ Tech Stack
FastAPI — web framework

SQLAlchemy — ORM

PostgreSQL — database

Docker Compose — container orchestration

📈 Roadmap
Planned enhancements:

🔐 Authentication & role-based access (JWT/OIDC)

📡 NVD JSON feed ingestion

🕵️ Asset discovery (Nmap integration)

🧩 Jira/ServiceNow ticket sync for remediation workflows

📊 UI dashboard for executives & analysts

🤝 Contributing
This project is in early MVP stage. Contributions, issues, and feature requests are welcome.
Feel free to fork, submit PRs, or open issues.