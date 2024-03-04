"""길드 랭킹 정보 조회 API를 제공하는 모듈입니다.

Note:
    - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
    - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
    - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
"""

from collections import defaultdict

import maplestory.utils.kst as kst
from maplestory.apis.ranking import get_guild_ranking_by_id
from maplestory.enums import GuildRankTypeEnum
from maplestory.models.ranking.guild import AllGuildRankingInfo, GuildTypeRanking
from maplestory.models.types import WorldName


def get_world_guild_ranking(
    world_name: WorldName,
    ranking_type: int | GuildRankTypeEnum = GuildRankTypeEnum.주간명성치,
    page_number: int = 1,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> GuildTypeRanking:
    """길드 랭킹 정보를 조회합니다.

    Args:
        world_name (str): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2, 버닝, 버닝2, 버닝3
        ranking_type (int | GuildRankType): 랭킹 타입 (0:주간 명성치, 1:플래그 레이스, 2:지하 수로)
        page_number : 페이지 번호
        date : 조회 기준일(KST)

    Returns:
        GuildRanking: 길드 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    return get_guild_ranking_by_id(
        ranking_type=ranking_type,
        world_name=world_name,
        page_number=page_number,
        date=date,
    )


def get_guild_ranking(
    guild: str,
    ranking_type: int | GuildRankTypeEnum = GuildRankTypeEnum.주간명성치,
    world_name: WorldName | None = None,
    page_number: int = 1,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> GuildTypeRanking:
    """길드 랭킹 정보를 조회합니다.

    Args:
        guild (str): 길드 명
        ranking_type (int | GuildRankType): 랭킹 타입 (0:주간 명성치, 1:플래그 레이스, 2:지하 수로)
        world_name (str, optional): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2, 버닝, 버닝2, 버닝3
        page_number : 페이지 번호
        date : 조회 기준일(KST)

    Returns:
        GuildRanking: 길드 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    return get_guild_ranking_by_id(
        ranking_type=ranking_type,
        world_name=world_name,
        guild=guild,
        page_number=page_number,
        date=date,
    )


def group_by_guild(all_rankings: list[dict]) -> dict:
    datas_by_key = defaultdict(list)
    for ranking in all_rankings:
        key = f"{ranking['guild_name']} ({ranking['world_name']})"
        datas_by_key[key].append(ranking)
    return dict(datas_by_key)


def get_all_type_guild_ranking(
    guild: str,
    world_name: WorldName | None = None,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> AllGuildRankingInfo:
    """길드 랭킹 정보를 조회합니다.

    Args:
        guild (str): 길드 명
        ranking_type (int | GuildRankType): 랭킹 타입 (0:주간 명성치, 1:플래그 레이스, 2:지하 수로)
        world_name (str, optional): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2, 버닝, 버닝2, 버닝3
        date : 조회 기준일(KST)

    Returns:
        AllGuildRankingInfo: 길드 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    all_rankings = []
    for ranking_type in [
        GuildRankTypeEnum.주간명성치,
        GuildRankTypeEnum.플래그레이스,
        GuildRankTypeEnum.지하수로,
    ]:
        result = get_guild_ranking_by_id(
            ranking_type=ranking_type, world_name=world_name, guild=guild, date=date
        )
        all_rankings.extend(result.model_dump()["ranking"])

    group_by_guild(all_rankings)
    # {
    #     '온앤온 (스카니아)': [
    #         {
    #             'date': '2024-02-25',
    #             'ranking': 25279,
    #             'guild_name': '온앤온',
    #             'world_name': '스카니아',
    #             'guild_level': 11,
    #             'guild_master_name': '온앤온',
    #             'guild_mark': '',
    #             'guild_point': 11600,
    #             'type': <GuildRankTypeEnum.WEEKLY_FAME: 0>
    #         },
    #         {
    #             'date': '2024-02-25',
    #             'ranking': 3721,
    #             'guild_name': '온앤온',
    #             'world_name': '스카니아',
    #             'guild_level': 11,
    #             'guild_master_name': '온앤온',
    #             'guild_mark': '',
    #             'guild_point': 15596,
    #             'type': <GuildRankTypeEnum.SEWER: 2>
    #         }
    #     ]
    # }

    all_data = {"ranking": all_rankings}
    # all_data = {
    #     'ranking': [
    #         {
    #             'date': '2024-02-25',
    #             'ranking': 25279,
    #             'guild_name': '온앤온',
    #             'world_name': '스카니아',
    #             'guild_level': 11,
    #             'guild_master_name': '온앤온',
    #             'guild_mark': '',
    #             'guild_point': 11600,
    #             'type': <GuildRankTypeEnum.주간명성치: 0>
    #         },
    #         {
    #             'date': '2024-02-25',
    #             'ranking': 3721,
    #             'guild_name': '온앤온',
    #             'world_name': '스카니아',
    #             'guild_level': 11,
    #             'guild_master_name': '온앤온',
    #             'guild_mark': '',
    #             'guild_point': 15596,
    #             'type': <GuildRankTypeEnum.지하수로: 2>
    #         }
    #     ]
    # }

    return AllGuildRankingInfo.from_dict(all_data)


def get_weekly_fame_guild_ranking(
    world_name: WorldName | None = None,
    guild: str | None = None,
    page_number: int = 1,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> GuildTypeRanking:
    """길드 랭킹 정보를 조회합니다.

    Args:
        world_name (str, optional): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2, 버닝, 버닝2, 버닝3
        guild (str, optional): 길드 명
        page_number : 페이지 번호
        date : 조회 기준일(KST)

    Returns:
        GuildRanking: 길드 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """
    return get_guild_ranking_by_id(
        ranking_type=GuildRankTypeEnum.주간명성치,
        world_name=world_name,
        guild=guild,
        page_number=page_number,
        date=date,
    )


def get_flag_race_guild_ranking(
    world_name: WorldName | None = None,
    guild: str | None = None,
    page_number: int = 1,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> GuildTypeRanking:
    """길드 랭킹 정보를 조회합니다.

    Args:
        world_name (str, optional): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2, 버닝, 버닝2, 버닝3
        guild (str, optional): 길드 명
        page_number : 페이지 번호
        date : 조회 기준일(KST)

    Returns:
        GuildRanking: 길드 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """
    return get_guild_ranking_by_id(
        ranking_type=GuildRankTypeEnum.플래그레이스,
        world_name=world_name,
        guild=guild,
        page_number=page_number,
        date=date,
    )


def get_sewer_guild_ranking(
    world_name: WorldName | None = None,
    guild: str | None = None,
    page_number: int = 1,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> GuildTypeRanking:
    """길드 랭킹 정보를 조회합니다.

    Args:
        world_name (str, optional): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2, 버닝, 버닝2, 버닝3
        guild (str, optional): 길드 명
        page_number : 페이지 번호
        date : 조회 기준일(KST)

    Returns:
        GuildRanking: 길드 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """
    return get_guild_ranking_by_id(
        ranking_type=GuildRankTypeEnum.지하수로,
        world_name=world_name,
        guild=guild,
        page_number=page_number,
        date=date,
    )
