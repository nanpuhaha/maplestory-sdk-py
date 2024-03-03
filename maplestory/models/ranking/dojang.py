from datetime import datetime

from pydantic import BaseModel, Field, field_validator

import maplestory.utils.kst as kst
from maplestory.enums import DojangDifficultyEnum
from maplestory.models.ranking.common import RankingModel
from maplestory.utils.repr import DatetimeRepresentation


class DojangRankingInfo(DatetimeRepresentation, BaseModel):
    """무릉도장 랭킹 상세 정보

    Attributes:
        date: 랭킹 업데이트 일자 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        ranking: 무릉도장 랭킹 순위
        character_name: 캐릭터 명
        world_name: 월드 명
        class_name: 직업 명
        sub_class_name: 전직 직업 명
        character_level: 캐릭터 레벨
        dojang_floor: 무릉도장 층수
        dojang_time_record: 무릉도장 클리어 시간 기록 (초 단위)
    """

    date: kst.KSTAwareDatetime
    ranking: int
    character_name: str
    world_name: str
    class_name: str
    sub_class_name: str
    character_level: int
    floor: int = Field(alias="dojang_floor")
    time_record: int = Field(alias="dojang_time_record")
    difficulty: DojangDifficultyEnum

    @field_validator("date", mode="before")
    @classmethod
    def change_date(cls, v: str) -> kst.KSTAwareDatetime:
        dt = datetime.strptime(v, "%Y-%m-%d")
        return kst.datetime(dt.year, dt.month, dt.day)

    @property
    def record(self) -> str:
        """무릉도장 클리어 시간 기록 (분:초)

        Returns:
            str: 무릉도장 클리어 시간 기록 (분:초)
        """
        minutes, seconds = divmod(self.time_record, 60)
        return f"{minutes:02d}분 {seconds:02d}초"


class DojangRanking(RankingModel[DojangRankingInfo]):
    """무릉도장 랭킹 정보

    Attributes:
        ranking: 무릉도장 랭킹 정보
    """
