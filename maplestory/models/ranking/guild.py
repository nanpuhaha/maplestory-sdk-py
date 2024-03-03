from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

import maplestory.utils.kst as kst
from maplestory.enums import GuildRankTypeEnum
from maplestory.models.ranking.common import RankingModel
from maplestory.utils.repr import DatetimeRepresentation

RankingType = dict[str, str | int | GuildRankTypeEnum]
RankingListType = list[RankingType]
RankByType = dict[str, RankingListType]


class GuildRankingInfo(DatetimeRepresentation, BaseModel):
    """길드 랭킹 상세 정보

    Attributes:
        date: 랭킹 업데이트 일자 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        ranking: 길드 랭킹 순위
        guild_name: 길드 명
        world_name: 월드 명
        guild_level: 길드 레벨
        guild_master_name: 길드 마스터 캐릭터 명
        guild_mark: 길드 마크
        guild_point: 길드 포인트
    """

    date: kst.KSTAwareDatetime
    ranking: int
    guild_name: str
    world_name: str
    guild_level: int
    guild_master_name: str
    guild_mark: str
    guild_point: int

    @field_validator("date", mode="before")
    @classmethod
    def change_date(cls, v: str) -> kst.KSTAwareDatetime:
        """
        Change the date format to a KSTAwareDatetime object.

        Args:
            v (str): The date string in the format "YYYY-MM-DD".

        Returns:
            kst.KSTAwareDatetime: The converted date as a KSTAwareDatetime object.

        Raises:
            TypeError: If the input is not a valid datetime object or does not have the KST timezone.

        Example:
            >>> change_date("2022-01-01")
            KSTAwareDatetime(2022, 1, 1, 0, 0, 0, tzinfo=KST_TZ)
        """

        if isinstance(v, datetime):
            return v

        dt = datetime.strptime(v, "%Y-%m-%d")
        return kst.datetime(dt.year, dt.month, dt.day)


class GuildRanking(RankingModel[GuildRankingInfo]):
    """길드 랭킹 정보

    Attributes:
        ranking: 길드 랭킹 정보
    """

    def set_rank_type(self, type: GuildRankTypeEnum):
        """
        Set the rank type for all guild ranking information.

        Args:
            type (GuildRankTypeEnum): The rank type to set for all guild ranking information.

        Returns:
            GuildRanking: The updated GuildRanking object with the rank type set for all guild ranking information.
        """

        for info in self.ranking:
            info.type = type
        return self


class GuildTypeRankingInfo(GuildRankingInfo):
    """길드 랭킹 상세 정보

    Attributes:
        date: 랭킹 업데이트 일자 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        ranking: 길드 랭킹 순위
        guild_name: 길드 명
        world_name: 월드 명
        guild_level: 길드 레벨
        guild_master_name: 길드 마스터 캐릭터 명
        guild_mark: 길드 마크
        guild_point: 길드 포인트
        type: 랭킹 타입
    """

    type: GuildRankTypeEnum

    @classmethod
    def from_info(
        cls, info: GuildRankingInfo, type: GuildRankTypeEnum
    ) -> GuildTypeRankingInfo:
        """
        Create a new instance of GuildTypeRankingInfo from a GuildRankingInfo object and a GuildRankTypeEnum.

        Args:
            info (GuildRankingInfo): The GuildRankingInfo object to create the GuildTypeRankingInfo from.
            type (GuildRankTypeEnum): The GuildRankTypeEnum to assign to the 'type' attribute of the new GuildTypeRankingInfo instance.

        Returns:
            GuildTypeRankingInfo: A new instance of GuildTypeRankingInfo with the attributes copied from the GuildRankingInfo object and the 'type' attribute set to the provided GuildRankTypeEnum.

        Example:
            ```python
            info = GuildRankingInfo(date=kst.KSTAwareDatetime(2022, 1, 1, 0, 0, 0, tzinfo=kst.KST_TZ), ranking=1, guild_name="Guild", world_name="World", guild_level=10, guild_master_name="Master", guild_mark="Mark", guild_point=100)
            type = GuildRankTypeEnum.WEEKLY_FAME
            result = GuildTypeRankingInfo.from_info(info, type)
            # result is a new instance of GuildTypeRankingInfo with the attributes copied from 'info' and the 'type' attribute set to GuildRankTypeEnum.WEEKLY_FAME.
            ```
        """

        data = info.model_dump()
        data["type"] = type
        return cls(**data)


class GuildTypeRanking(RankingModel[GuildTypeRankingInfo]):
    """길드 랭킹 정보

    Attributes:
        ranking: 길드 랭킹 정보
    """

    @classmethod
    def from_ranking(
        cls, ranking: GuildRanking, rank_type: GuildRankTypeEnum
    ) -> GuildTypeRanking:
        """Create a GuildTypeRanking instance from a GuildRanking instance and a GuildRankTypeEnum.

        Args:
            ranking (GuildRanking): The GuildRanking instance to create from.
            rank_type (GuildRankTypeEnum): The GuildRankTypeEnum to assign to each ranking data.

        Returns:
            GuildTypeRanking: The created GuildTypeRanking instance.
        """

        data = ranking.model_dump()
        for info in data["ranking"]:
            info["type"] = rank_type

        return cls(**data)


class GuildRankingTypePoint(BaseModel):
    """길드 랭킹 정보

    Attributes:
        rank: 길드 랭킹 순위
        point: 점수
    """

    rank: int = Field(alias="ranking")
    point: int = Field(alias="guild_point")

    model_config = {"extra": "ignore"}


class AllGuildRankingInfo(DatetimeRepresentation, BaseModel):
    """길드 랭킹 상세 정보

    Attributes:
        date: 랭킹 업데이트 일자 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        ranking: 길드 랭킹 순위
        guild_name: 길드 명
        world_name: 월드 명
        guild_level: 길드 레벨
        guild_master_name: 길드 마스터 캐릭터 명
        guild_mark: 길드 마크
        guild_point: 길드 포인트
    """

    date: kst.KSTAwareDatetime
    guild_name: str
    world_name: str
    guild_level: int
    guild_master_name: str
    guild_mark: str
    flag_race: GuildRankingTypePoint | None = None
    weekly_fame: GuildRankingTypePoint | None = None
    sewer: GuildRankingTypePoint | None = None

    @property
    def 주간명성치(self) -> GuildRankingTypePoint | None:
        return self.weekly_fame

    @property
    def 플레그레이스(self) -> GuildRankingTypePoint | None:
        return self.flag_race

    @property
    def 지하수로(self) -> GuildRankingTypePoint | None:
        return self.sewer

    @classmethod
    def from_dict(cls, rank_by_type: RankByType) -> AllGuildRankingInfo:
        """
        Converts a dictionary representation of guild ranking information into an instance of the 'AllGuildRankingInfo' class.

        Parameters:
            rank_by_type (RankByType): A dictionary containing the guild ranking information.

        Returns:
            AllGuildRankingInfo: An instance of the 'AllGuildRankingInfo' class representing the guild ranking information.

        Examples:
            ```python
            >>> AllGuildRankingInfo.from_dict(rank_by_type={
                'ranking': [
                    {
                        'date': '2024-02-25',
                        'ranking': 25279,
                        'guild_name': '온앤온',
                        'world_name': '스카니아',
                        'guild_level': 11,
                        'guild_master_name': '온앤온',
                        'guild_mark': '',
                        'guild_point': 11600,
                        'type': GuildRankTypeEnum.주간명성치
                    },
                    {
                        'date': '2024-02-25',
                        'ranking': 3721,
                        'guild_name': '온앤온',
                        'world_name': '스카니아',
                        'guild_level': 11,
                        'guild_master_name': '온앤온',
                        'guild_mark': '',
                        'guild_point': 15596,
                        'type': GuildRankTypeEnum.지하수로
                    }
                ]
            })

            AllGuildRankingInfo(
                date='2024-02-25',
                guild_name='온앤온',
                world_name='스카니아',
                guild_level=11,
                guild_master_name='온앤온',
                guild_mark='',
                flag_race=None,
                weekly_fame=GuildRankingTypePoint(rank=25279, point=11600),
                sewer=GuildRankingTypePoint(rank=3721, point=15596)
            )
            ```
        """

        rank_types = [rank.name.lower() for rank in GuildRankTypeEnum]
        data = {}
        for rank in rank_by_type["ranking"]:
            try:
                data[rank_types[rank["type"].value]] = rank
            except KeyError:
                continue

        weekly_fame_data = data.get("weekly_fame", {})

        data["date"] = weekly_fame_data.get("date")
        data["guild_name"] = weekly_fame_data.get("guild_name")
        data["world_name"] = weekly_fame_data.get("world_name")
        data["guild_level"] = weekly_fame_data.get("guild_level")
        data["guild_master_name"] = weekly_fame_data.get("guild_master_name")
        data["guild_mark"] = weekly_fame_data.get("guild_mark")

        return cls(**data)


class AllGuildRanking(RankingModel[AllGuildRankingInfo]):
    """길드 랭킹 정보

    Attributes:
        ranking: 길드 랭킹 정보
    """
