"""이 모듈은 한국 표준시(KST)에 대한 날짜와 시간을 처리하는 함수와 클래스를 제공합니다.

- `KSTAwareDatetime` 클래스는 한국 표준시(KST) 시간대 정보를 요구하는 datetime을 나타냅니다.
- `validate` 함수는 주어진 datetime이 한국 표준시(KST) 시간대 정보를 가지고 있는지 확인합니다.
- `now`, `yesterday`, `datetime` 함수는 각각 현재, 어제, 주어진 시간의 한국 표준시(KST)을 반환합니다.
"""

from datetime import datetime as _datetime
from datetime import timedelta, timezone
from functools import wraps
from typing import Annotated, Callable
from zoneinfo import ZoneInfo

from annotated_types import Interval, Timezone

KST_TZ = ZoneInfo("Asia/Seoul")
KST_TZ_CONSTRAINT = 9 * 60 * 60
KSTAwareDatetime = Annotated[_datetime, Timezone("Asia/Seoul")]
Year = Annotated[int, Interval(ge=1, le=9999)]
Month = Annotated[int, Interval(ge=1, le=12)]
Day = Annotated[int, Interval(ge=1, le=31)]
Hour = Annotated[int, Interval(ge=0, le=23)]
Minute = Annotated[int, Interval(ge=0, le=59)]
Second = Annotated[int, Interval(ge=0, le=59)]
Microsecond = Annotated[int, Interval(ge=0, le=999999)]


def is_aware(dt: _datetime) -> bool:
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


def is_naive(dt: _datetime) -> bool:
    return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None


def is_kst_timezone(tzinfo) -> bool:
    if tzinfo in [KST_TZ, timezone(timedelta(seconds=32400))]:
        return True
    elif tzinfo is not None and tzinfo.utcoffset(None) == timedelta(hours=9):
        return True
    return False


def is_kst_datetime(dt: _datetime) -> bool:
    return is_kst_timezone(dt.tzinfo)


def ensure_kst_aware_datetime(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> KSTAwareDatetime:
        result = func(*args, **kwargs)
        if not isinstance(result, _datetime) or not is_kst_timezone(result.tzinfo):
            raise TypeError("Return value is not a KSTAwareDatetime")
        return result

    return wrapper


@ensure_kst_aware_datetime
def to_kst(dt: _datetime) -> KSTAwareDatetime:
    if is_aware(dt):
        return dt.astimezone(KST_TZ)
    else:
        return dt.replace(tzinfo=timezone.utc).astimezone(KST_TZ)


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
    year: Year,
    month: Month,
    day: Day,
    hour: Hour = 0,
    minute: Minute = 0,
    second: Second = 0,
    microsecond: Microsecond = 0,
) -> KSTAwareDatetime:
    """주어진 시간의 한국 표준시(KST)를 반환합니다."""
    return _datetime(year, month, day, hour, minute, second, microsecond, tzinfo=KST_TZ)


def today_with_time(hour=0, minute=0) -> KSTAwareDatetime:
    _today = today()
    return datetime(_today.year, _today.month, _today.day, hour, minute)


def is_same_date(date1: KSTAwareDatetime, date2: KSTAwareDatetime) -> bool:
    return date1.date() == date2.date()
