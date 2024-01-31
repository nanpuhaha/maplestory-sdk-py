"""이 모듈은 Pydantic의 BaseModel을 상속받은 클래스에서 특정 조건을 만족하는 필드를 `__repr__` 메소드의 결과에서 제외하는 기능을 제공합니다.

- `HideNoneRepresentation` 믹스인 클래스는 `None` 값을 가진 필드를 제외합니다.
- `HideZeroStatRepresentation` 믹스인 클래스는 "STR", "INT", "DEX", "LUK" 키에 대응하는 값이 0인 필드를 제외합니다.
"""

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pydantic_core import TzInfo

from maplestory.utils.kst import KST_TZ_CONSTRAINT


class HideNoneRepresentation:
    """`None` 값을 가진 필드를 `__repr__` 메서드의 결과에서 제외하는 믹스인 클래스입니다."""

    def __repr_args__(self: BaseModel):
        """BaseModel의 `__repr__` 메서드에서 사용하는 필드와 값의 리스트를 반환합니다.

        이 메서드는 `None` 값을 가진 필드를 제외합니다.

        Returns:
            list: 필드 이름과 값의 튜플을 원소로 가지는 리스트입니다. `None` 값을 가진 필드는 제외됩니다.
        """
        return [
            (key, value) for key, value in self.__dict__.items() if value is not None
        ]


class HideZeroStatRepresentation:
    """스탯 값이 0인 경우를 `__repr__` 메서드의 결과에서 제외하는 믹스인 클래스입니다."""

    STAT_KEYS = ["STR", "INT", "DEX", "LUK", "HP"]

    def __repr_args__(self: BaseModel):
        """BaseModel의 `__repr__` 메소드에서 사용하는 필드와 값의 리스트를 반환하는데, 스탯 값이 0인 필드를 제외합니다.

        Returns:
            list: 스탯 값이 0인 필드가 제외된 필드 이름과 값의 튜플을 원소로 가지는 리스트입니다.
        """

        return [
            (key, value)
            for key, value in self.__dict__.items()
            if key not in self.STAT_KEYS or value != 0
        ]


class DatetimeRepresentation:
    def convert_datetime_as_sstr(self, value: Any):
        if not isinstance(value, datetime):
            return value

        tz = ""
        if value.tzinfo in [ZoneInfo(key="Asia/Seoul"), TzInfo(KST_TZ_CONSTRAINT)]:
            tz = " KST"

        if value.hour or value.minute or value.second:
            return value.strftime(f"%Y-%m-%d %H:%M:%S{tz}")

        return value.strftime(f"%Y-%m-%d{tz}")

    def __repr_args__(self: BaseModel):
        for k, v in self.__dict__.items():
            field = self.model_fields.get(k)
            if field and field.repr:
                yield k, self.convert_datetime_as_sstr(v)

        try:
            pydantic_extra = object.__getattribute__(self, "__pydantic_extra__")
        except AttributeError:
            pydantic_extra = None

        if pydantic_extra is not None:
            yield from ((k, v) for k, v in pydantic_extra.items())
        yield from (
            (k, getattr(self, k))
            for k, v in self.model_computed_fields.items()
            if v.repr
        )
