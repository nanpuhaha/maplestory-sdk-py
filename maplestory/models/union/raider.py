from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class UnionRaiderBlockPosition(BaseModel):
    """블록이 차지하고 있는 영역 좌표들

    Attributes:
        x: 블록 X좌표
        y: 블록 Y좌표
    """

    x: int
    y: int


class UnionRaiderBlockControlPoint(BaseModel):
    """블록 기준점 좌표

    Attributes:
        x: 블록 기준점 X좌표
        y: 블록 기준점 Y좌표

    Notes:
        - 중앙 4칸 중 오른쪽 아래 칸이 x=0, y=0 포지션
        - 좌측으로 1칸씩 이동하면 x가 1씩 감소
        - 우측으로 1칸씩 이동하면 x가 1씩 증가
        - 아래로 1칸씩 이동하면 y가 1씩 감소
        - 위로 1칸씩 이동하면 y가 1씩 증가
    """

    x: int
    y: int


class UnionRaiderBlock(BaseModel):
    """유니온 블록 배치 정보

    Attributes:
        type: 블록 모양 (전사, 마법사, 궁수, 도적, 해적, 메이플M, 하이브리드)
        character_class: 블록 해당 캐릭터 직업
        level: 블록 해당 캐릭터 레벨
        control_point: 블록 기준점 좌표
        position: 블록이 차지하고 있는 영역 좌표들
    """

    type: str = Field(alias="block_type")
    character_class: str = Field(alias="block_class")
    level: str = Field(alias="block_level")
    control_point: UnionRaiderBlockControlPoint = Field(alias="block_control_point")
    position: list[UnionRaiderBlockPosition] = Field(alias="block_position")


class UnionRaiderInnerStat(BaseModel):
    """유니온 공격대 안쪽 지역 효과 배치 정보

    Attributes:
        stat_field_id: 공격대 배치 위치 (11시 방향부터 시계 방향 순서대로 0~7)
        stat_field_effect: 해당 지역 점령 효과

    Examples:
        {
            "stat_field_id": "0",
            "stat_field_effect": "유니온 STR"
        },
        {
            "stat_field_id": "4",
            "stat_field_effect": "유니온 공격력"
        },
        {
            "stat_field_id": "6",
            "stat_field_effect": "유니온 최대 HP"
        }
    """

    stat_field_id: str
    stat_field_effect: str


class UnionRaider(BaseModel):
    """유니온 공격대 정보

    Attributes:
        date: 조회 기준일 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        raider_stats: 유니온 공격대원 효과
        occupied_stats: 유니온 공격대 점령 효과
        inner_stats: 유니온 공격대 안쪽 지역 효과 정보
        blocks: 유니온 블록 배치 정보
    """

    date: datetime = Field(repr=False)
    raider_stats: list[str] = Field(alias="union_raider_stat")
    occupied_stats: list[str] = Field(alias="union_occupied_stat")
    inner_stats: list[UnionRaiderInnerStat] = Field(alias="union_inner_stat")
    blocks: list[UnionRaiderBlock] = Field(alias="union_block")

    def model_post_init(self, __context: Any) -> None:
        self.raider_stats = sorted(self.raider_stats)
        self.occupied_stats = sorted(self.occupied_stats)

    @property
    def 공격대원_효과(self) -> list[str]:
        return self.raider_stats

    @property
    def 공격대_점령_효과(self) -> list[str]:
        return self.occupied_stats
