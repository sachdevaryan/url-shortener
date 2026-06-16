from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.database import get_db
from app.models import URL
from app.schemas import ShortenRequest, ShortenResponse, StatsResponse
from app.utils import generate_short_code
import os

router = APIRouter()

@router.post("/shorten", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest, db: Session = Depends(get_db)):
    # Collision check loop
    for _ in range(5):
        code = generate_short_code()
        if not db.query(URL).filter(URL.short_code == code).first():
            break
    else:
        raise HTTPException(status_code=500, detail="Could not generate unique code")

    url_entry = URL(original_url=str(request.url), short_code=code)
    db.add(url_entry)
    db.commit()
    db.refresh(url_entry)

    base_url = os.getenv("BASE_URL", "http://localhost")
    return ShortenResponse(short_code=code, short_url=f"{base_url}/{code}")


@router.get("/stats/{code}", response_model=StatsResponse)
def get_stats(code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short code not found")
    return url_entry


@router.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short code not found")

    db.execute(
        update(URL).where(URL.short_code == code).values(click_count=URL.click_count + 1)
    )
    db.commit()

    return RedirectResponse(url=url_entry.original_url, status_code=301)
