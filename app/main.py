# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from .routers import assets, findings, health

app = FastAPI(
    title="Sparkwave-Insight",
    version="0.1.0",
    docs_url=None,   # we'll mount a custom /docs
    redoc_url=None,  # and a custom /redoc
)

# Static assets (CSS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# MVP: create tables (switch to Alembic later)
Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <link rel="stylesheet" href="/static/css/brand.css">
        <title>Sparkwave-Insight</title>
      </head>
      <body style="margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto;">
        <div style="background: var(--brand-secondary); padding: 20px;">
          <div style="max-width:960px; margin:0 auto; display:flex; align-items:center; gap:14px;">
            <img src="/static/img/logo.png" alt="Sparkwave IT" style="height:32px" onerror="this.style.display='none'">
            <h1 style="margin:0; color:var(--brand-text);">Sparkwave-Insight</h1>
          </div>
        </div>
        <div style="max-width:960px; margin: 24px auto; color:var(--brand-text);">
          <p>Mission-first vulnerability management MVP. Visit <a href="/docs">/docs</a> for the API.</p>
        </div>
      </body>
    </html>
    """

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Sparkwave-Insight — API Docs",
        swagger_favicon_url="/static/img/logo.png",  # optional
        oauth2_redirect_url=None,
        init_oauth=None,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        # Inject our CSS after Swagger's CSS
        # FastAPI helper doesn’t have a param for “extra CSS”, so we append via <link> using a simple wrapper below
    )

@app.get("/redoc", include_in_schema=False)
def custom_redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Sparkwave-Insight — ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

# Inject our CSS into /docs by overriding the HTML response (tiny middleware-ish trick)
@app.middleware("http")
async def brand_swagger_css(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/docs" and isinstance(response, HTMLResponse):
        html = response.body.decode("utf-8")
        # add our stylesheet before closing </head>
        branded = html.replace(
            "</head>",
            '<link rel="stylesheet" type="text/css" href="/static/css/brand.css"></head>',
        )
        return HTMLResponse(content=branded, status_code=response.status_code)
    return response

# Routers
app.include_router(health.router)
app.include_router(assets.router)
app.include_router(findings.router)

from .routers import assets, findings, health, feeds
# ...
app.include_router(feeds.router)
