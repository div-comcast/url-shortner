from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.models import Analytics, Url


class UrlRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_long_url(self, url: str) -> Url | None:
        return self.session.query(Url).filter(Url.long_url == url).first()

    def get_by_code(self, code: str) -> Url | None:
        return self.session.query(Url).filter(Url.code == code).first()

    def save(self, code: str, long_url: str, short_url: str) -> Url:
        row = Url(code=code, long_url=long_url, short_url=short_url)
        self.session.add(row)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise
        return row

    def save_analytics(self, click) -> None:
        """Persist one click event. `click` is a ClickDataResponse."""
        row = Analytics(
            code=click.code,
            clicked_at=click.clicked_at,
            ip=click.ip,
            country=click.country,
            city=click.city,
            device=click.device,
            browser=click.browser,
            os=click.os,
            referrer=click.referrer,
        )
        self.session.add(row)
        self.session.commit()
