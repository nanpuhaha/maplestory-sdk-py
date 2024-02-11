from datetime import datetime

from pydantic import BaseModel, Field


class CharacterStatInfo(BaseModel):
    """캐릭터 스탯 상세 정보

    Attributes:
        name (str): 스탯 이름
        value (str): 스탯 값
    """

    name: str = Field(alias="stat_name")
    value: int | float = Field(alias="stat_value")


class CharacterStat(BaseModel):
    """캐릭터 스탯 정보

    Attributes:
        date (datetime): 조회 기준일
        character_class (str): 직업
        stats (list[CharacterStatInfo]): 현재 스탯 정보
        remain_ap (int): 잔여 AP
    """

    date: datetime = Field(repr=False)
    character_class: str
    stats: list[CharacterStatInfo] = Field(alias="final_stat")
    remain_ap: int
