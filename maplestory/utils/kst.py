"""이 모듈은 한국 표준시(KST)에 대한 날짜와 시간을 처리하는 함수와 클래스를 제공합니다.

- `KSTAwareDatetime` 클래스는 한국 표준시(KST) 시간대 정보를 요구하는 datetime을 나타냅니다.
- `validate` 함수는 주어진 datetime이 한국 표준시(KST) 시간대 정보를 가지고 있는지 확인합니다.
- `now`, `yesterday`, `datetime` 함수는 각각 현재, 어제, 주어진 시간의 한국 표준시(KST)을 반환합니다.
"""

from datetime import datetime as _datetime
from datetime import timedelta
from typing import Annotated
from zoneinfo import ZoneInfo

from annotated_types import Timezone

KST_TZ = ZoneInfo("Asia/Seoul")
KST_TZ_CONSTRAINT = 9 * 60 * 60
KSTAwareDatetime = Annotated[_datetime, Timezone("Asia/Seoul")]


def validate(date: _datetime):
    """주어진 날짜가 한국 표준시(KST) 시간대 정보를 가지고 있는지 확인합니다."""
    if date.tzinfo is None:
        raise ValueError("datetime should have timezone info.")

    if date.tzinfo.utcoffset(date) != timedelta(seconds=KST_TZ_CONSTRAINT):
        raise ValueError("datetime should have KST timezone info.")


def now() -> KSTAwareDatetime:
    """현재 한국 표준시(KST) 시간을 반환합니다."""
    return _datetime.now(KST_TZ)


def today() -> KSTAwareDatetime:
    """어제의 한국 표준시(KST) 시간을 반환합니다."""
    today_kst = _datetime.now(KST_TZ)
    return datetime(today_kst.year, today_kst.month, today_kst.day)


def yesterday() -> KSTAwareDatetime:
    """어제의 한국 표준시(KST) 시간을 반환합니다."""
    today_kst = _datetime.now(KST_TZ)
    yesterday_kst = today_kst - timedelta(days=1)
    return datetime(yesterday_kst.year, yesterday_kst.month, yesterday_kst.day)


def datetime(
    year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0
) -> KSTAwareDatetime:
    """주어진 시간의 한국 표준시(KST)를 반환합니다."""
    return _datetime(year, month, day, hour, minute, second, microsecond, tzinfo=KST_TZ)


def today_with_time(hour=0, minute=0) -> KSTAwareDatetime:
    _today = today()
    return datetime(_today.year, _today.month, _today.day, hour, minute)


def is_same_date(date1: KSTAwareDatetime, date2: KSTAwareDatetime) -> bool:
    return date1.date() == date2.date()
