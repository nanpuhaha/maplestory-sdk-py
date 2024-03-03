from datetime import datetime, timedelta, timezone

import pytest

import maplestory.utils.kst as kst
from maplestory.enums import QueryableDateEnum
from maplestory.utils.date import is_valid, to_string


class TestToString:
    # Returns a string in the default format when given a valid datetime object.
    def test_returns_default_format(self):
        date = datetime(2022, 1, 1)
        result = to_string(date)

        assert isinstance(result, str)
        assert result == "2022-01-01"

    # Returns a string in the specified format when given a valid datetime object and a valid format string.
    def test_returns_specified_format(self):
        date = datetime(2022, 1, 1)
        format = "%d/%m/%Y"
        result = to_string(date, format)

        assert isinstance(result, str)
        assert result == "01/01/2022"

    # Returns None when given None as the datetime object.
    def test_returns_none_with_none_date(self):
        date = None
        result = to_string(date)
        assert result is None

    # Returns None when given an empty string as the format string.
    def test_returns_none_with_empty_format(self):
        date = datetime(2022, 1, 1)
        format = ""
        result = to_string(date, format)
        assert result == ""

    # Returns None when given an invalid format string.
    def test_returns_none_with_invalid_format(self):
        date = datetime(2022, 1, 1)
        format = "%d-%m-%Y %H:%M:%S"
        result = to_string(date, format)
        assert result == "01-01-2022 00:00:00"

    # Returns None when given an object that is not a datetime object.
    def test_returns_none_with_non_datetime_object(self):
        with pytest.raises(ValueError, match=r".*Invalid date type*"):
            date = "2022-01-01"
            _ = to_string(date)


class TestIsValid:
    def test_invalid_date(self):
        category = QueryableDateEnum.캐릭터
        invalid_date = category.value - timedelta(days=1)

        with pytest.raises(
            ValueError,
            match=r"CHARACTER{은,는} 2023-12-21부터 데이터를 조회할 수 있습니다.",
        ):
            _ = is_valid(invalid_date, category)

    # Verify that a valid date for a given category does not raise any exception
    def test_valid_date_no_exception(self):
        valid_date = kst.datetime(2023, 12, 21)
        category = QueryableDateEnum.캐릭터

        try:
            is_valid(valid_date, category)
        except ValueError:
            pytest.fail("Unexpected ValueError raised")

    # Verify that a date equal to the minimum date for a given category does not raise any exception
    def test_minimum_date_no_exception(self):
        minimum_date = QueryableDateEnum.캐릭터.value
        category = QueryableDateEnum.캐릭터

        try:
            is_valid(minimum_date, category)
        except ValueError:
            pytest.fail("Unexpected ValueError raised")

    # Verify that a date greater than the minimum date for a given category does not raise any exception
    def test_greater_than_minimum_date_no_exception(self):
        greater_date = kst.datetime(2024, 1, 1)
        category = QueryableDateEnum.캐릭터

        try:
            is_valid(greater_date, category)
        except ValueError:
            pytest.fail("Unexpected ValueError raised")

    # Verify that a date with timezone other than KST raises a ValueError
    def test_timezone_value_error(self):
        invalid_date = datetime(2023, 12, 21, tzinfo=timezone.utc)
        category = QueryableDateEnum.캐릭터

        with pytest.raises(ValueError):
            is_valid(invalid_date, category)

    # Verify that a date with no timezone raises a ValueError
    def test_no_timezone_value_error(self):
        invalid_date = datetime(2023, 12, 21)
        category = QueryableDateEnum.캐릭터

        with pytest.raises(ValueError):
            is_valid(invalid_date, category)

    # Verify that a date with timezone other than KST and a date with no timezone raise different ValueErrors
    def test_different_value_errors(self):
        invalid_date_with_timezone = datetime(2023, 12, 21, tzinfo=timezone.utc)
        invalid_date_no_timezone = datetime(2023, 12, 21)
        category = QueryableDateEnum.캐릭터

        with pytest.raises(ValueError) as exc_info:
            is_valid(invalid_date_with_timezone, category)
        error_with_timezone = exc_info.value

        with pytest.raises(ValueError) as exc_info:
            is_valid(invalid_date_no_timezone, category)
        error_no_timezone = exc_info.value

        assert error_with_timezone != error_no_timezone
