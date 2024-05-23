from datetime import UTC, datetime


class Datetime:
    @classmethod
    def now(cls) -> datetime:
        return datetime.now(UTC).replace(microsecond=0)
