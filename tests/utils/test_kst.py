from datetime import datetime as _datetime
from datetime import timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from maplestory.utils.kst import (
    KST_TZ,
    datetime,
    ensure_kst_aware_datetime,
    is_aware,
    is_kst_datetime,
    is_kst_timezone,
    is_naive,
    now,
    to_kst,
    validate,
)


class TestIsAware:
    # Tests if a timezone-aware datetime object is correctly identified
    def test_aware_datetime_recognition(self):
        dt = _datetime(2022, 1, 1, tzinfo=timezone.utc)
        assert is_aware(dt)

    # Tests if a datetime object becomes naive after removing its timezone information
    def test_naive_after_removing_timezone(self):
        dt = _datetime(2022, 1, 1, tzinfo=timezone.utc).replace(tzinfo=None)
        assert not is_aware(dt)

    # Tests if a naive datetime object (without timezone) is correctly identified
    def test_recognition_of_naive_datetime(self):
        dt = _datetime(2022, 1, 1)
        assert not is_aware(dt)


class TestIsNaive:
    # Tests if a naive datetime object is correctly identified
    def test_naive_datetime_recognition(self):
        dt = _datetime(2022, 1, 1)
        assert is_naive(dt)

    # Tests if a datetime object with UTC timezone is not considered naive
    def test_datetime_with_utc_not_naive(self):
        dt = _datetime(2022, 1, 1, tzinfo=timezone.utc)
        assert not is_naive(dt)

    # Tests if a datetime object with KST timezone is not considered naive
    def test_datetime_with_kst_not_naive(self):
        dt = _datetime(2022, 1, 1, tzinfo=KST_TZ)
        assert not is_naive(dt)


class TestIsKstTimezone:
    # Tests if KST timezone is correctly identified
    def test_kst_timezone_identification(self):
        assert is_kst_timezone(KST_TZ)
        assert is_kst_timezone(ZoneInfo("Asia/Seoul"))
        assert is_kst_timezone(timezone(timedelta(hours=9)))

    # Tests if non-KST timezones are correctly identified as not KST
    def test_non_kst_timezone_identification(self):
        assert not is_kst_timezone(ZoneInfo("Europe/Copenhagen"))
        assert not is_kst_timezone(timezone(timedelta(hours=1)))

    # Tests if None is correctly identified as not a KST timezone
    def test_none_as_not_kst_timezone(self):
        assert not is_kst_timezone(None)


class TestIsKstDatetime:
    # Tests if a datetime object with KST timezone is correctly identified
    def test_kst_timezone_datetime_recognition(self):
        dt = _datetime.now(timezone(timedelta(seconds=32400)))
        assert is_kst_datetime(dt) is True

        dt = _datetime.now(tz=KST_TZ)
        assert is_kst_datetime(dt) is True

    # Tests error handling for None input
    def test_error_for_none_input(self):
        with pytest.raises(
            AttributeError, match="'NoneType' object has no attribute 'tzinfo'"
        ):
            _ = is_kst_datetime(None)

    # Tests if datetime objects with a different timezone are identified as not KST
    def test_non_kst_timezone_datetime_recognition(self):
        dt = _datetime.now(timezone.utc)
        assert not is_kst_datetime(dt)

    # Tests if naive datetime objects are identified as not KST
    def test_naive_datetime_recognition_as_not_kst(self):
        dt = _datetime.now()
        assert not is_kst_datetime(dt)


class TestEnsureKstAwareDatetime:
    # Ensures that the wrapped function returns a KSTAwareDatetime object with valid timezone.
    def test_valid_timezone(self):
        @ensure_kst_aware_datetime
        def func():
            return datetime(2022, 1, 1)

        result = func()
        assert isinstance(result, _datetime)
        assert is_kst_timezone(result.tzinfo)
        assert result.tzinfo == KST_TZ or result.tzinfo.utcoffset(result) == timedelta(
            hours=9
        )

    # Tests handling of a datetime object with an incorrect timezone
    def test_handle_incorrect_timezone(self):
        @ensure_kst_aware_datetime
        def func():
            return _datetime(2022, 1, 1, tzinfo=timezone(timedelta(hours=8)))  # Not KST

        with pytest.raises(
            TypeError
            # TypeError, match="The datetime object is not in KST timezone."
        ):
            func()

    # Tests that a correct KST datetime object is passed through without modification
    def test_correct_kst_datetime_pass_through(self):
        @ensure_kst_aware_datetime
        def func():
            return _datetime(2022, 1, 1, tzinfo=KST_TZ)

        result = func()
        assert result.tzinfo == KST_TZ or result.tzinfo.utcoffset(result) == timedelta(
            hours=9
        )

    # Tests that an appropriate exception is raised if the function returns None
    def test_exception_for_none_return_value(self):
        @ensure_kst_aware_datetime
        def func():
            return None

        # with pytest.raises(TypeError, match="Return value is not a datetime object"):
        with pytest.raises(TypeError):
            func()


class TestToKst:
    # Tests conversion of a valid datetime object to KST
    def test_convert_to_kst_timezone(self):
        dt = _datetime(2022, 1, 1, 12, 0, tzinfo=timezone.utc)
        result = to_kst(dt)
        assert result.tzinfo == KST_TZ or result.tzinfo.utcoffset(result) == timedelta(
            hours=9
        )

    # Tests raising an error when provided with a non-datetime object
    def test_error_on_non_datetime_input(self):
        with pytest.raises(
            AttributeError, match="'str' object has no attribute 'tzinfo'"
        ):
            to_kst("2022-01-01")

    # Tests converting a naive datetime object to KST
    def test_convert_naive_datetime_to_kst(self):
        dt = _datetime(2022, 1, 1, 12)
        result = to_kst(dt)
        assert result.tzinfo == KST_TZ


class TestNow:
    # Tests returning the current datetime in KST timezone
    def test_current_datetime_in_kst(self):
        result = now()
        assert isinstance(result, _datetime)
        assert result.tzinfo == ZoneInfo("Asia/Seoul")

    # Tests that the function returns a datetime object
    def test_return_type_is_datetime(self):
        result = now()
        assert isinstance(result, _datetime)


class TestDatetime:
    # Tests that the datetime constructor correctly assigns all components and KST timezone
    def test_datetime_constructor_with_kst_timezone(self):
        result = _datetime(2022, 10, 15, 12, 30, 45, 500, tzinfo=KST_TZ)
        assert result.year == 2022 and result.month == 10 and result.day == 15
        assert (
            result.hour == 12
            and result.minute == 30
            and result.second == 45
            and result.microsecond == 500
        )
        assert result.tzinfo == KST_TZ

    # Tests that providing a non-integer year to the datetime constructor raises a TypeError
    def test_year_as_non_integer_raises_type_error(self):
        with pytest.raises(TypeError):
            _datetime("2022", 10, 15)

    # Tests that providing a year outside the valid range [1, 9999] raises a ValueError
    def test_year_out_of_valid_range_raises_value_error(self):
        with pytest.raises(ValueError):
            _datetime(0, 10, 15)
        with pytest.raises(ValueError):
            _datetime(10000, 10, 15)

    # Tests that providing a non-integer month to the datetime constructor raises a TypeError
    def test_month_as_non_integer_raises_type_error(self):
        with pytest.raises(TypeError):
            _datetime(2022, "10", 15)


class TestValidate:
    # Tests that validate function does not raise error for datetime with KST timezone
    def test_validate_with_kst_timezone(self):
        date = _datetime(2022, 1, 1, tzinfo=KST_TZ)
        try:
            validate(date)
        except ValueError as e:
            pytest.fail(f"Unexpected ValueError raised: {e}")

    # Tests that validate function does not raise error for datetime with equivalent to KST timezone
    def test_validate_with_equivalent_to_kst_timezone(self):
        date = _datetime(2022, 1, 1, tzinfo=timezone(timedelta(hours=9)))
        try:
            validate(date)
        except ValueError as e:
            pytest.fail(f"Unexpected ValueError raised: {e}")

    # Tests that validate function raises error for datetime with non-KST timezone
    def test_validate_with_non_kst_timezone_raises_error(self):
        date = _datetime(
            2022, 1, 1, tzinfo=timezone(timedelta(hours=8))
        )  # Example: UTC+8
        with pytest.raises(ValueError, match="datetime should have KST timezone info."):
            validate(date)

    # Tests that validate function raises error for naive datetime objects
    def test_validate_with_naive_datetime_raises_error(self):
        date = _datetime(2022, 1, 1)  # No timezone info
        with pytest.raises(ValueError, match="datetime should have timezone info."):
            validate(date)
