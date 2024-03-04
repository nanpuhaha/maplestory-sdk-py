"""업적 랭킹 정보 조회 API를 제공하는 모듈입니다.

Note:
    - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
    - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
    - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
"""

import maplestory.utils.kst as kst
from maplestory.apis.ranking import get_achievement_ranking_by_id
from maplestory.models.ranking import AchievementRanking
from maplestory.models.ranking.achievement import AchievementRankingInfo
from maplestory.services.character import get_character_id


def get_achievement_ranking(
    character_name: str | None = None,
    page_number: int = 1,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> AchievementRanking:
    """조회 기준일(KST)과 캐릭터명를 사용하여 업적 랭킹 정보를 조회합니다.

    Args:
        character_name (str): 캐릭터명.
        page_number (int): 페이지 번호.
        date (datetime): 조회 기준일(KST)

    Returns:
        AchievementRanking: 업적 랭킹 정보.

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    character_id = get_character_id(character_name) if character_name else None
    return get_achievement_ranking_by_id(character_id, page_number, date)


def get_character_achievement_rank(
    character_name: str,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> AchievementRankingInfo | None:
    """조회 기준일(KST)과 캐릭터명를 사용하여 업적 랭킹 정보를 조회합니다.

    Args:
        character_name (str): 캐릭터명.
        date (datetime): 조회 기준일(KST)

    Returns:
        AchievementRankingInfo: 업적 랭킹 정보.

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    rank = get_achievement_ranking(character_name=character_name, date=date)
    return rank[0] if len(rank) == 1 else None
