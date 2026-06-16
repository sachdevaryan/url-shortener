# URL Shortener

![CI](https://github.com/sachdevaryan/url-shortener/actions/workflows/ci.yml/badge.svg)

A production-grade URL shortener built with FastAPI, PostgreSQL, Docker, and Nginx. The app itself is simple — the goal is the infrastructure around it.

## Architecture

Client → Nginx (port 80) → FastAPI/uvicorn (port 8000) → PostgreSQL

## Tech Stack

![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-multi--stage-2496ED?logo=docker)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions)

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shorten` | Accept a long URL, return a short code |
| GET | `/{code}` | Redirect to original URL, increment click count |
| GET | `/stats/{code}` | Return original URL, click count, created_at |

## How to Run

```bash
cp .env.example .env        # fill in your values
docker-compose up --build   # starts Postgres + FastAPI + Nginx
```

Then try it:

```bash
# Shorten a URL
curl -X POST http://localhost/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}'

# Redirect (follow the 301)
curl -L http://localhost/{code}

# Get stats
curl http://localhost/stats/{code}
```

## Run Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## CI/CD Pipeline

Every push to `main`:
1. GitHub Actions spins up a real Postgres service container
2. Runs all tests against it
3. On success, builds the Docker image and pushes to GHCR

Docker image: `ghcr.io/sachdevaryan/url-shortener:latest`

