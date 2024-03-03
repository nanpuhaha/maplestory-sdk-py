from datetime import datetime

from pydantic import BaseModel, Field, field_validator

import maplestory.utils.kst as kst
from maplestory.models.ranking.common import RankingModel
from maplestory.utils.repr import DatetimeRepresentation


class OverallRankingInfo(DatetimeRepresentation, BaseModel):
    """종합 랭킹 상세 정보

    Attributes:
        date: 랭킹 업데이트 일자 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        ranking: 종합 랭킹 순위
        character_name: 캐릭터 명
        world_name: 월드 명
        class_name: 직업 명
        sub_class_name: 전직 직업 명
        character_level: 캐릭터 레벨
        character_exp: 캐릭터 경험치
        character_popularity: 캐릭터 인기도
        character_guildname: 길드 명
    """

    date: kst.KSTAwareDatetime
    ranking: int
    character_name: str
    world_name: str
    class_name: str  # FIXME: RankingCharacterClass
    sub_class_name: str  # FIXME: RankingCharacterSubClass
    character_level: int
    character_exp: int
    popularity: int = Field(alias="character_popularity")
    guild_name: str | None = Field(alias="character_guildname")

    @field_validator("date", mode="before")
    @classmethod
    def change_date(cls, v: str) -> kst.KSTAwareDatetime:
        dt = datetime.strptime(v, "%Y-%m-%d")
        return kst.datetime(dt.year, dt.month, dt.day)

    @property
    def 레벨(self) -> int:
        return self.character_level

    @property
    def 경험치(self) -> int:
        return self.character_exp

    @property
    def 인기도(self) -> int:
        return self.popularity

    @property
    def 길드명(self) -> str | None:
        return self.guild_name


class OverallRanking(RankingModel[OverallRankingInfo]):
    """종합 랭킹 정보

    Attributes:
        ranking: 종합 랭킹 정보
    """

    @property
    def world_names(self) -> set[str]:
        return {rank.world_name for rank in self.ranking}

    @property
    def class_names(self) -> set[str]:
        return {rank.class_name for rank in self.ranking}

    @property
    def sub_class_names(self) -> set[str]:
        return {rank.sub_class_name for rank in self.ranking}
