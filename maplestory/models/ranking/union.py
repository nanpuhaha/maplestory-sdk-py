from datetime import datetime

from pydantic import BaseModel, field_validator

import maplestory.utils.kst as kst
from maplestory.models.ranking.common import RankingModel
from maplestory.types.union import UnionWorldName


class UnionRankingInfo(BaseModel):
    """유니온 랭킹 상세 정보

    Attributes:
        date: 랭킹 업데이트 일자 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        ranking: 유니온 랭킹 순위
        character_name: 캐릭터 명
        world_name: 월드 명
        class_name: 직업 명
        sub_class_name: 전직 직업 명
        union_level: 유니온 레벨
        union_power: 유니온 파워
    """

    date: kst.KSTAwareDatetime
    ranking: int
    character_name: str
    world_name: UnionWorldName
    class_name: str
    sub_class_name: str
    union_level: int
    union_power: int

    @field_validator("date", mode="before")
    @classmethod
    def change_date(cls, v: str) -> kst.KSTAwareDatetime:
        dt = datetime.strptime(v, "%Y-%m-%d")
        return kst.datetime(dt.year, dt.month, dt.day)


class UnionRanking(RankingModel[UnionRankingInfo]):
    """유니온 랭킹 정보

    Attributes:
        ranking: 유니온 랭킹 정보
    """
