from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from pydantic import BaseModel
from pydantic_core import TzInfo

from maplestory.utils.kst import KST_TZ_CONSTRAINT
from maplestory.utils.repr import (
    DatetimeRepresentation,
    HideNoneRepresentation,
    HideZeroStatRepresentation,
    convert_datetime_as_str,
)


class TestHideNoneRepresentation:

    # The __repr_args__ method returns a list of tuples containing field names and their values, excluding those with None values.
    def test_repr_args_excludes_none_values(self):
        class TestModel(HideNoneRepresentation, BaseModel):
            field1: str
            field2: int
            field3: float | None

        instance = TestModel(field1="value1", field2=2, field3=None)

        assert instance.__repr_args__() == [("field1", "value1"), ("field2", 2)]

    # BaseModel is properly inherited and used in the class.
    def test_base_model_inherited_and_used(self):
        class TestModel(HideNoneRepresentation, BaseModel):
            field1: str
            field2: int

        instance = TestModel(field1="value1", field2=2)

        assert isinstance(instance, TestModel)
        assert isinstance(instance, BaseModel)
        assert repr(instance) == "TestModel(field1='value1', field2=2)"

    # The class can be instantiated without any arguments.
    def test_instantiate_without_arguments(self):
        class TestModel(HideNoneRepresentation, BaseModel):
            field1: str | None
            field2: int

        instance = TestModel(field1=None, field2=2)

        assert isinstance(instance, TestModel)
        assert isinstance(instance, BaseModel)
        assert repr(instance) == "TestModel(field2=2)"

    # The class is instantiated with arguments that have None values.
    def test_instantiate_with_none_values(self):
        class TestModel(HideNoneRepresentation, BaseModel):
            field1: str | None
            field2: int | None

        instance = TestModel(field1=None, field2=None)

        assert isinstance(instance, TestModel)
        assert repr(instance) == "TestModel()"

    # The __repr__ method is called on an instance with no arguments.
    def test_repr_called_on_instance_without_arguments(self):
        class TestModel(HideNoneRepresentation, BaseModel):
            field1: str | None = None
            field2: int | None = None

        instance = TestModel()

        assert isinstance(instance, TestModel)
        assert repr(instance) == "TestModel()"

    # The class is instantiated with arguments that have non-None values and None values.
    def test_instantiate_with_mixed_values(self):
        class TestModel(HideNoneRepresentation, BaseModel):
            field1: str
            field2: int | None

        instance = TestModel(field1="value1", field2=None)

        assert isinstance(instance, TestModel)
        assert repr(instance) == "TestModel(field1='value1')"


class TestHideZeroStatRepresentation:

    # The __repr_args__ method returns a list of tuples containing field names and values, excluding fields with a value of 0.
    def test_repr_args_excludes_fields_with_value_of_0(self):
        class TestModel(HideZeroStatRepresentation, BaseModel):
            STR: int
            DEX: int
            INT: int
            LUK: int
            HP: int

        instance = TestModel(STR=0, DEX=1, INT=0, LUK=2, HP=0)

        assert instance.__repr_args__() == [("DEX", 1), ("LUK", 2)]
        assert repr(instance) == "TestModel(DEX=1, LUK=2)"

    # All fields have a value of 0.
    def test_all_fields_have_value_of_0(self):
        class TestModel(HideZeroStatRepresentation, BaseModel):
            STR: int
            DEX: int
            INT: int
            LUK: int
            HP: int

        instance = TestModel(STR=0, DEX=0, INT=0, LUK=0, HP=0)

        assert instance.__repr_args__() == []
        assert repr(instance) == "TestModel()"

    # All fields have a non-zero value.
    def test_all_fields_have_non_zero_value(self):
        class TestModel(HideZeroStatRepresentation, BaseModel):
            STR: int
            DEX: int
            INT: int
            LUK: int
            HP: int

        instance = TestModel(STR=100, DEX=80, INT=10, LUK=20, HP=1000)

        assert instance.__repr_args__() == [
            ("STR", 100),
            ("DEX", 80),
            ("INT", 10),
            ("LUK", 20),
            ("HP", 1000),
        ]
        assert repr(instance) == "TestModel(STR=100, DEX=80, INT=10, LUK=20, HP=1000)"

    # The class is instantiated with arguments that are not in the STAT_KEYS list.
    def test_instantiation_with_arguments_not_in_STAT_KEYS_list(self):
        class AnotherTestModel(HideZeroStatRepresentation, BaseModel):
            field1: int
            field2: int
            field3: int
            field4: int

        instance = AnotherTestModel(field1=1, field2=0, field3=3, field4=0)

        assert instance.__repr_args__() == [
            ("field1", 1),
            ("field2", 0),
            ("field3", 3),
            ("field4", 0),
        ]

    # The class can be instantiated without any arguments.
    def test_instantiation_without_arguments(self):
        hide_zero_stat = HideZeroStatRepresentation()

        assert isinstance(hide_zero_stat, HideZeroStatRepresentation)

    # The class can be subclassed without any issues.
    def test_subclassing_without_issues(self):
        class SubHideZeroStatRepresentation(HideZeroStatRepresentation):
            pass

        sub_hide_zero_stat = SubHideZeroStatRepresentation()

        assert isinstance(sub_hide_zero_stat, HideZeroStatRepresentation)


class TestConvertDatetimeAsStr:

    def test_convert_datetime_without_timezone(self):
        """Test converting a datetime object without a timezone."""
        dt = datetime(2022, 1, 1, 15, 30, 45)
        expected = "2022-01-01 15:30:45"
        assert convert_datetime_as_str(dt) == expected

    def test_convert_datetime_with_kst_timezone(self):
        """Test converting a datetime object with the KST timezone."""
        kst = ZoneInfo("Asia/Seoul")
        dt = datetime(2022, 1, 1, 15, 30, 45, tzinfo=kst)
        expected = "2022-01-01 15:30:45 KST"
        assert convert_datetime_as_str(dt) == expected

        kst = TzInfo(KST_TZ_CONSTRAINT)
        dt = datetime(2022, 1, 1, 15, 30, 45, tzinfo=kst)
        expected = "2022-01-01 15:30:45 KST"
        assert convert_datetime_as_str(dt) == expected

    def test_convert_non_datetime_value(self):
        """Test converting a non-datetime value."""
        non_dt_value = "2022-01-01"
        assert convert_datetime_as_str(non_dt_value) == non_dt_value

    # Should raise "ValueError: year 0 is out of range." if the input datetime has a timezone of 'Asia/Seoul' or 'KST_TZ_CONSTRAINT' and has zero year, month, day, hour, minute and second
    def test_raise_value_error_if_zero_year_month_day_hour_minute_second(
        self,
    ):
        with pytest.raises(ValueError, match=r".*year 0 is out of range.*"):
            _ = datetime(0, 0, 0, tzinfo=ZoneInfo(key="Asia/Seoul"))

    # Should raise "ValueError: year 0 is out of range." if the input datetime has no timezone and has zero year, month, day, hour, minute and second
    def test_raise_value_error_if_no_timezone_and_zero_year_month_day_hour_minute_second(
        self,
    ):
        with pytest.raises(ValueError, match=r".*year 0 is out of range.*"):
            _ = datetime(0, 0, 0)


class TestDatetimeRepresentation:

    def test_without_timezone(self):
        class TestModel(DatetimeRepresentation, BaseModel):
            name: str
            date: datetime

        instance = TestModel(name="Test Name", date=datetime(2022, 1, 1))

        assert list(instance.__repr_args__()) == [
            ("name", "Test Name"),
            ("date", "2022-01-01"),
        ]
        assert repr(instance) == "TestModel(name='Test Name', date='2022-01-01')"

    def test_with_seoul_zoneinfo(self):
        class TestModel(DatetimeRepresentation, BaseModel):
            name: str
            date: datetime

        instance = TestModel(
            name="Test Name", date=datetime(2022, 1, 1, tzinfo=ZoneInfo("Asia/Seoul"))
        )

        assert list(instance.__repr_args__()) == [
            ("name", "Test Name"),
            ("date", "2022-01-01 KST"),
        ]
        assert repr(instance) == "TestModel(name='Test Name', date='2022-01-01 KST')"

    def test_with_kst_timezone(self):
        class TestModel(DatetimeRepresentation, BaseModel):
            name: str
            date: datetime

        instance = TestModel(
            name="Test Name",
            date=datetime(2022, 1, 1, tzinfo=TzInfo(KST_TZ_CONSTRAINT)),
        )

        assert list(instance.__repr_args__()) == [
            ("name", "Test Name"),
            ("date", "2022-01-01 KST"),
        ]
        assert repr(instance) == "TestModel(name='Test Name', date='2022-01-01 KST')"

    def test_with_utc_timezone(self):
        class TestModel(DatetimeRepresentation, BaseModel):
            name: str
            date: datetime

        instance = TestModel(
            name="Test Name", date=datetime(2022, 1, 1, tzinfo=ZoneInfo("UTC"))
        )

        assert list(instance.__repr_args__()) == [
            ("name", "Test Name"),
            ("date", "2022-01-01"),
        ]
        assert repr(instance) == "TestModel(name='Test Name', date='2022-01-01')"
