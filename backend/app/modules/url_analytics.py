import datetime
import pytz

from fastapi import Request
from sqlalchemy.orm import Session

from app.modules.schema import AnalyticsResponse
from app.repositories.url_repository import UrlRepository

import user_agents

IST = pytz.timezone("Asia/Kolkata")


class UrlAnalytics:

    def parse_click_data(self, code: str, request: Request) -> AnalyticsResponse:
        ip = request.client.host if request.client else None

        raw_ua = request.headers.get("user-agent", "")
        device, browser, os_name = None, None, None

        if raw_ua:
            ua = user_agents.parse(raw_ua)
            if ua.is_mobile:
                device = "Mobile"
            elif ua.is_tablet:
                device = "Tablet"
            else:
                device = "Desktop"
            browser = ua.browser.family or None
            os_name = ua.os.family or None

        raw_referrer = request.headers.get("referer") or request.headers.get("referrer")
        referrer = self._parse_referrer(raw_referrer)

        return AnalyticsResponse(
            code=code,
            clicked_at=datetime.datetime.now(IST),
            ip=ip,
            device=device,
            browser=browser,
            os=os_name,
            referrer=referrer,
            country=None,
            city=None,
        )

    def _parse_referrer(self, raw: str | None) -> str | None:
        if not raw:
            return "Direct"
        raw = raw.lower()
        if "google" in raw:
            return "Google"
        if "twitter" in raw or "t.co" in raw:
            return "Twitter"
        if "linkedin" in raw:
            return "LinkedIn"
        if "facebook" in raw or "fb.com" in raw:
            return "Facebook"
        if "instagram" in raw:
            return "Instagram"
        if "youtube" in raw:
            return "YouTube"
        return raw


def run_url_analytics(code: str, request: Request, db: Session) -> AnalyticsResponse:
    click = UrlAnalytics().parse_click_data(code, request)
    UrlRepository(db).save_analytics(click)
    return click
