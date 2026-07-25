import datetime
from pydantic import BaseModel


class ShortenResponse(BaseModel):
    short_url: str
    code: str


class AnalyticsResponse(BaseModel):
    code: str
    clicked_at: datetime.datetime
    ip: str | None
    device: str | None
    browser: str | None
    os: str | None
    referrer: str | None
    country: str | None
    city: str | None

    class Config:
        from_attributes = True
