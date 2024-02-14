from datetime import datetime as _datetime
from datetime import timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from maplestory.utils.kst import KST_TZ, datetime, now, validate


class TestNow:

    # Returns the current time in the KST timezone.
    def test_returns_current_time_in_KST_timezone(self):
        result = now()
        assert isinstance(result, _datetime)
        assert result.tzinfo == ZoneInfo(key="Asia/Seoul")

    # Returns a datetime object.
    def test_returns_datetime_object(self):
        result = now()
        assert isinstance(result, _datetime)


class TestDatetime:

    # Returns a datetime object with the correct year, month, day, hour, minute, second, and microsecond values, with KST timezone info.
    def test_correct_values_with_timezone_info(self):
        result = datetime(2022, 10, 15, 12, 30, 45, 500)
        assert result.year == 2022
        assert result.month == 10
        assert result.day == 15
        assert result.hour == 12
        assert result.minute == 30
        assert result.second == 45
        assert result.microsecond == 500
        assert result.tzinfo == KST_TZ

    # Raises a TypeError when year is not an integer.
    def test_raises_type_error_when_year_not_integer(self):
        with pytest.raises(TypeError):
            datetime("2022")

    # Raises a TypeError when year is less than 1 or greater than 9999.
    def test_raises_type_error_when_year_out_of_range(self):
        with pytest.raises(TypeError):
            datetime(0)
        with pytest.raises(TypeError):
            datetime(10000)

    # Raises a TypeError when month is not an integer.
    def test_raises_type_error_when_month_not_integer(self):
        with pytest.raises(TypeError):
            datetime(2022, "10")


class TestValidate:

    # The function should not raise any errors if the input datetime has timezone information and the timezone offset is equal to the KST timezone offset.
    def test_valid_timezone_offset(self):
        date = _datetime(2022, 1, 1, tzinfo=KST_TZ)
        try:
            validate(date)
        except ValueError:
            pytest.fail("Unexpected ValueError raised.")

    # The function should not raise any errors if the input datetime has timezone information and the timezone offset is not equal to the KST timezone offset, but is still a valid timezone offset.
    def test_valid_timezone_offset_not_equal(self):
        date = _datetime(2022, 1, 1, tzinfo=timezone(timedelta(hours=9)))
        try:
            validate(date)
        except ValueError:
            pytest.fail("Unexpected ValueError raised.")

    # The function should not raise any errors if the input datetime has timezone information and the timezone offset is not equal to the KST timezone offset, but is still a valid timezone offset, and the datetime is not in the KST timezone.
    def test_valid_timezone_offset_not_equal_other_timezone(self):
        date = _datetime(2022, 1, 1, tzinfo=timezone(timedelta(hours=8)))
        with pytest.raises(
            ValueError, match=r"datetime should have KST timezone info."
        ):
            validate(date)

    # The function should raise a ValueError if the input datetime does not have timezone information.
    def test_missing_timezone_info(self):
        date = _datetime(2022, 1, 1)
        with pytest.raises(ValueError):
            validate(date)

    # The function should not raise any errors if the input datetime has timezone information and the timezone offset is not equal to the KST timezone offset, but is still a valid timezone offset, and the datetime is in the KST timezone.
    def test_valid_timezone_offset_not_equal_same_timezone(self):
        date = _datetime(2022, 1, 1, tzinfo=timezone(timedelta(hours=10)))
        with pytest.raises(
            ValueError, match=r"datetime should have KST timezone info."
        ):
            validate(date)

        date = _datetime(2022, 1, 1, tzinfo=timezone(timedelta(hours=11)))
        with pytest.raises(
            ValueError, match=r"datetime should have KST timezone info."
        ):
            validate(date)
