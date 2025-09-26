# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

# --- DB & models ---
from .db import Base, engine
from . import models  # IMPORTANT: import models BEFORE create_all so tables get registered

# --- Routers ---
from .routers import assets, findings, health, feeds


app = FastAPI(
    title="Sparkwave-Insight",
    version="0.1.0",
    docs_url=None,   # we'll serve a custom /docs
    redoc_url=None,  # and a custom /redoc
)

# Static assets (CSS/logo). check_dir=False so startup doesn't crash if the folder is missing.
app.mount("/static", StaticFiles(directory="app/static", check_dir=False), name="static")

# Create tables (MVP). Replace with Alembic migrations when schema stabilizes.
Base.metadata.create_all(bind=engine)


# ---------- Simple branded landing ----------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Sparkwave-Insight</title>
        <link rel="stylesheet" href="/static/css/brand.css" />
        <style>
          body { margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; }
          .top { background: var(--brand-secondary, #1e293b); padding: 16px; }
          .wrap { max-width: 960px; margin: 0 auto; color: var(--brand-text, #e5e7eb); }
          .cta a { display:inline-block; margin-top:12px; padding:10px 14px;
                   background: var(--brand-primary, #0ea5e9); color:#0b1220; text-decoration:none; border-radius:8px; }
        </style>
      </head>
      <body>
        <div class="top">
          <div class="wrap">
            <h1 style="margin:0">Sparkwave-Insight</h1>
            <div class="cta"><a href="/docs">Open API Docs</a></div>
          </div>
        </div>
        <div class="wrap" style="padding:24px">
          <p>Mission-first vulnerability management MVP. Health at <code>/health/</code>.</p>
        </div>
      </body>
    </html>
    """


# ---------- Custom-branded Swagger & ReDoc ----------
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    # Use CDN for Swagger UI assets; we’ll inject our CSS via middleware below.
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Sparkwave-Insight — API Docs",
        swagger_favicon_url="/static/img/logo.png",  # optional; ignored if file not present
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/redoc", include_in_schema=False)
def custom_redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Sparkwave-Insight — ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )


# Inject our brand.css into the /docs HTML
@app.middleware("http")
async def brand_swagger_css(request: Request, call_next):
    resp = await call_next(request)
    if request.url.path == "/docs" and isinstance(resp, HTMLResponse):
        html = resp.body.decode("utf-8")
        branded = html.replace(
            "</head>",
            '<link rel="stylesheet" type="text/css" href="/static/css/brand.css"></head>',
        )
        return HTMLResponse(content=branded, status_code=resp.status_code, headers=dict(resp.headers))
    return resp


# ---------- Register routers ----------
app.include_router(health.router)
app.include_router(assets.router)
app.include_router(findings.router)
app.include_router(feeds.router)
