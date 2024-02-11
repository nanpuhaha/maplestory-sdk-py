import re
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, computed_field, field_validator

from ..types import ArtifactCrystalOption

StatTuple = tuple[str, int | float]
UNION_ARTIFACT_MAX_LEVEL = 10


def parse_stat_string(stat_str: str) -> StatTuple | list[StatTuple]:
    """
    Parse a string containing stat information and return the parsed results.

    Args:
        stat_str (str): The string containing the stat information.

    Returns:
        StatTuple | list[StatTuple]: The parsed results.
            If the stat_str matches the pattern and contains a single stat, a tuple with the stat name and value is returned.
            If the stat_str matches the pattern and contains multiple stats, a list of tuples with the stat names and values is returned.

    Raises:
        ValueError: If the stat_str does not match the pattern.

    Examples:
        >>> parse_stat_string("올스탯 150 증가")
        ('올스탯', 150)

        >>> parse_stat_string("공격력 18, 마력 18 증가")
        [('공격력', 18), ('마력', 18)]

        >>> parse_stat_string("데미지 15.00% 증가")
        ('데미지', 0.15)

        >>> parse_stat_string("보스 몬스터 공격 시 데미지 15.00% 증가")
        ('보스 몬스터 공격 시 데미지', 0.15)

        >>> parse_stat_string("몬스터 방어율 무시 20% 증가")
        ('몬스터 방어율 무시', 0.2)

        >>> parse_stat_string("아이템 드롭률 7% 증가")
        ('아이템 드롭률', 0.07)

        >>> parse_stat_string("크리티컬 데미지 2.40% 증가")
        ('크리티컬 데미지', 0.024)
    """

    stat_pattern = r"([가-힣\s]+)\s(\d+(\.\d+)?%?)?(\s증가)?"

    matches = re.findall(stat_pattern, stat_str)
    if not matches:
        raise ValueError(f"Invalid stat string: {stat_str}")

    results = []
    for match in matches:
        stat_name = match[0].strip()
        stat_value = match[1]

        if stat_value is None:
            raise ValueError(f"Invalid stat string: {stat_str}")
        elif "%" in stat_value:
            stat_value = float(stat_value.rstrip("%")) / 100.0
            results.append((stat_name, stat_value))
        else:
            results.append((stat_name, int(stat_value)))

    return results[0] if len(results) == 1 else results


class UnionArtifactEffect(BaseModel):
    """유니온 아티팩트 효과 정보

    Attributes:
        name: 아티팩트 효과 명
        level: 아티팩트 효과 레벨

    Examples:
        {
            "name": "올스탯 150 증가",
            "level": 10
        },
        {
            "name": "데미지 15.00% 증가",
            "level": 10
        },
        {
            "name": "보스 몬스터 공격 시 데미지 15.00% 증가",
            "level": 10
        },
        {
            "name": "몬스터 방어율 무시 20% 증가",
            "level": 10
        },
        {
            "name": "버프 지속시간 20% 증가",
            "level": 10
        },
        {
            "name": "아이템 드롭률 7% 증가",
            "level": 6
        },
        {
            "name": "크리티컬 확률 20% 증가",
            "level": 10
        },
        {
            "name": "크리티컬 데미지 2.40% 증가",
            "level": 6
        },
        {
            "name": "최대 HP 2250, 최대 MP 2250 증가",
            "level": 3
        },
        {
            "name": "공격력 30, 마력 30 증가",
            "level": 10
        },
        {
            "name": "재사용 대기시간 미적용 확률 7.50% 증가",
            "level": 10
        },
        {
            "name": "추가 경험치 획득 6% 증가, 다수 공격 스킬의 최대 공격 가능 대상 수 1 증가",
            "level": 5
        }
    """

    name: str
    level: int

    @property
    def stat(self) -> StatTuple | list[StatTuple]:
        return parse_stat_string(self.name)

    def is_max_level(self) -> bool:
        return self.level == UNION_ARTIFACT_MAX_LEVEL

    def required_ap_for_max_level(self) -> int:
        # TODO: Implement required AP calculation
        pass


class UnionArtifactCrystal(BaseModel):
    """유니온 아티팩트 크리스탈 정보

    Attributes:
        name: 아티팩트 크리스탈 명
        validity_flag: 능력치 유효 여부 (0:유효, 1:유효하지 않음)
        date_expire: 능력치 유효 기간(KST)
        level: 아티팩트 크리스탈 등급
        option_name_1: 아티팩트 크리스탈 첫 번째 옵션 명
        option_name_2: 아티팩트 크리스탈 두 번째 옵션 명
        option_name_3: 아티팩트 크리스탈 세 번째 옵션 명
    """

    name: str
    validity_flag: str = Field(repr=False)
    date_expire: datetime
    level: int
    option1: ArtifactCrystalOption = Field(alias="crystal_option_name_1", repr=False)
    option2: ArtifactCrystalOption = Field(alias="crystal_option_name_2", repr=False)
    option3: ArtifactCrystalOption = Field(alias="crystal_option_name_3", repr=False)

    @field_validator("date_expire", mode="before")
    @classmethod
    def make_date_expire(cls, v: Any) -> datetime:
        try:
            # 2024/02/20 19:26:00:000
            date = datetime.strptime(v, "%Y-%m-%dT%H:%M%z")
        except ValueError:
            # 2024-01-26T00:00+09:00
            try:
                date = datetime.strptime(v, "%Y/%m/%d %H:%M:%S:%f")
            except ValueError as error:
                raise error

        return date

    @computed_field
    def expired(self) -> bool:
        return self.validity_flag == "1"

    @computed_field(repr=False)
    def active(self) -> bool:
        return self.validity_flag == "0"

    valid = active

    @computed_field
    def options(self) -> list[ArtifactCrystalOption]:
        return [self.option1, self.option2, self.option3]

    @computed_field
    def remaining_time(self) -> int:
        return self.date_expire - datetime.now()

    @computed_field
    def remaining_time_str(self) -> int:
        days = self.remaining_time.days
        seconds = self.remaining_time.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{days}일 {hours}시간 {minutes}분 {seconds}초"

    @computed_field
    def remaining_time_short_str(self) -> int:
        days = self.remaining_time.days + self.remaining_time.seconds // 3600 / 24
        return f"{days:.1f}일"

    @computed_field
    def remaining_days(self) -> int:
        return (self.date_expire - datetime.now()).days


class UnionArtifactCrystalGrade(Enum):
    GRADE_1 = (0, 0)
    GRADE_2 = (1, 1)
    GRADE_3 = (2, 3)
    GRADE_4 = (2, 5)
    GRADE_5 = (3, 8)

    def __init__(self, consumed_ap, cumulative_ap):
        self.consumed_ap = consumed_ap
        self.cumulative_ap = cumulative_ap

    @property
    def required_ap_for_next_level(self) -> int:
        return self.consumed_ap

    @property
    def required_ap_for_max_level(self) -> int:
        return self.__class__.GRADE_5.cumulative_ap - self.cumulative_ap


class UnionArtifact(BaseModel):
    """유니온 아티팩트 정보

    Attributes:
        date: 조회 기준일 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        effects: 아티팩트 효과 정보
        crystals: 아티팩트 크리스탈 정보
        remain_ap: 잔여 아티팩트 AP
    """

    date: datetime = Field(repr=False)
    effects: list[UnionArtifactEffect] = Field(alias="union_artifact_effect")
    crystals: list[UnionArtifactCrystal] = Field(alias="union_artifact_crystal")
    remain_ap: int | None = Field(alias="union_artifact_remain_ap")
