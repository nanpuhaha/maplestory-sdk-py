"""유니온 랭킹 정보 조회 API를 제공하는 모듈입니다.

Note:
    - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
    - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
    - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
"""

import maplestory.utils.kst as kst
from maplestory.apis.ranking import get_union_ranking_by_id
from maplestory.models.ranking import UnionRanking
from maplestory.models.ranking.union import UnionRankingInfo
from maplestory.services.character import get_character_id
from maplestory.types.union import UnionWorldName


def get_union_ranking(
    world_name: UnionWorldName | None = None,
    character_name: str | None = None,
    page_number: int = 1,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> UnionRanking:
    """유니온 랭킹 정보를 조회합니다.

    Args:
        world (str, optional): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2
        character_name (str, optional): 캐릭터명
        page_number (int): 페이지 번호
        date (datetime): 조회 기준일(KST)

    Returns:
        UnionRanking: 유니온 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    character_id = get_character_id(character_name) if character_name else None
    return get_union_ranking_by_id(world_name, character_id, page_number, date)


def get_world_union_ranking(
    world_name: UnionWorldName,
    page_number: int = 1,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> UnionRanking:
    """유니온 랭킹 정보를 조회합니다.

    Args:
        world (str): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2
        page_number (int): 페이지 번호
        date (datetime): 조회 기준일(KST)

    Returns:
        UnionRanking: 유니온 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    return get_union_ranking_by_id(
        world_name=world_name, page_number=page_number, date=date
    )


def get_character_union_rank(
    character_name: str,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> UnionRankingInfo | None:
    """유니온 랭킹 정보를 조회합니다.

    Args:
        character_name (str): 캐릭터명
        date (datetime): 조회 기준일(KST)

    Returns:
        UnionRankingInfo: 유니온 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    rank = get_union_ranking(character_name=character_name, date=date)
    return rank[0] if len(rank) == 1 else None
