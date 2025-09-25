FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project metadata and source
COPY pyproject.toml ./
COPY app ./app
COPY .env.example ./

# Install build tools + your package (brings in FastAPI, Uvicorn, etc.)
RUN pip install --no-cache-dir --upgrade pip build \
    && pip install -e .

EXPOSE 8000
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
