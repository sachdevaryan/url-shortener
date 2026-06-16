from pydantic import BaseModel, HttpUrl
from datetime import datetime

class ShortenRequest(BaseModel):
    url: HttpUrl

class ShortenResponse(BaseModel):
    short_code: str
    short_url: str

class StatsResponse(BaseModel):
    original_url: str
    short_code: str
    click_count: int
    created_at: datetime