"""무릉도장 랭킹 정보 조회 API를 제공하는 모듈입니다.

Note:
    - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
    - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
    - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
"""

import maplestory.utils.kst as kst
from maplestory.apis.ranking import get_dojang_ranking_by_id
from maplestory.enums import DojangDifficultyEnum
from maplestory.models.ranking import DojangRanking
from maplestory.models.ranking.dojang import DojangRankingInfo
from maplestory.models.types import JobClass, WorldName
from maplestory.services.character import get_character_id


def get_dojang_ranking(
    world_name: WorldName | None = None,
    job_class: JobClass | None = None,
    character_name: str | None = None,
    page_number: int = 1,
    difficulty_level: int | DojangDifficultyEnum = DojangDifficultyEnum.통달,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> DojangRanking:
    """무릉도장 랭킹 정보를 조회합니다.

    Args:
        world_name (str): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2, 버닝, 버닝2, 버닝3
        job_class (str): 직업 및 전직
            Available values : 초보자-전체 전직, 전사-전체 전직, 전사-검사, 전사-파이터, 전사-페이지, 전사-스피어맨,
                전사-크루세이더, 전사-나이트, 전사-버서커, 전사-히어로, 전사-팔라딘, 전사-다크나이트, 마법사-전체 전직,
                마법사-매지션, 마법사-위자드(불,독), 마법사-위자드(썬,콜), 마법사-클레릭, 마법사-메이지(불,독),
                마법사-메이지(썬,콜), 마법사-프리스트, 마법사-아크메이지(불,독), 마법사-아크메이지(썬,콜), 마법사-비숍,
                궁수-전체 전직, 궁수-아처, 궁수-헌터, 궁수-사수, 궁수-레인저, 궁수-저격수, 궁수-보우마스터, 궁수-신궁,
                궁수-아처(패스파인더), 궁수-에인션트아처, 궁수-체이서, 궁수-패스파인더, 도적-전체 전직, 도적-로그, 도적-어쌔신,
                도적-시프, 도적-허밋, 도적-시프마스터, 도적-나이트로드, 도적-섀도어, 도적-세미듀어러, 도적-듀어러, 도적-듀얼마스터,
                도적-슬래셔, 도적-듀얼블레이더, 해적-전체 전직, 해적-해적, 해적-인파이터, 해적-건슬링거, 해적-캐논슈터,
                해적-버커니어, 해적-발키리, 해적-캐논블래스터, 해적-바이퍼, 해적-캡틴, 해적-캐논마스터, 기사단-전체 전직,
                기사단-노블레스, 기사단-소울마스터, 기사단-플레임위자드, 기사단-윈드브레이커, 기사단-나이트워커, 기사단-스트라이커,
                기사단-미하일, 아란-전체 전직, 에반-전체 전직, 레지스탕스-전체 전직, 레지스탕스-시티즌, 레지스탕스-배틀메이지,
                레지스탕스-와일드헌터, 레지스탕스-메카닉, 레지스탕스-데몬슬레이어, 레지스탕스-데몬어벤져, 레지스탕스-제논,
                레지스탕스-블래스터, 메르세데스-전체 전직, 팬텀-전체 전직, 루미너스-전체 전직, 카이저-전체 전직, 엔젤릭버스터-전체 전직,
                초월자-전체 전직, 초월자-제로, 은월-전체 전직, 프렌즈 월드-전체 전직, 프렌즈 월드-키네시스, 카데나-전체 전직,
                일리움-전체 전직, 아크-전체 전직, 호영-전체 전직, 아델-전체 전직, 카인-전체 전직, 라라-전체 전직, 칼리-전체 전직
        character_name (str): 캐릭터명
        page_number (int) : 페이지 번호
        difficulty_level (int): 구간 (0:일반, 1:통달)
        date (datetime): 조회 기준일(KST)

    Returns:
        DojangRanking: 무릉도장 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    character_id = get_character_id(character_name) if character_name else None

    return get_dojang_ranking_by_id(
        world_name, job_class, character_id, page_number, difficulty_level, date
    )


def get_world_dojang_ranking(
    world_name: str,
    job_class: JobClass | None = None,
    page_number: int = 1,
    difficulty_level: int | DojangDifficultyEnum = DojangDifficultyEnum.통달,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> DojangRanking:
    """무릉도장 랭킹 정보를 조회합니다.

    Args:
        world_name (str): 월드 명
            Available values : 스카니아, 베라, 루나, 제니스, 크로아, 유니온, 엘리시움,
                이노시스, 레드, 오로라, 아케인, 노바, 리부트, 리부트2, 버닝, 버닝2, 버닝3
        job_class (str): 직업 및 전직
            Available values : 초보자-전체 전직, 전사-전체 전직, 전사-검사, 전사-파이터, 전사-페이지, 전사-스피어맨,
                전사-크루세이더, 전사-나이트, 전사-버서커, 전사-히어로, 전사-팔라딘, 전사-다크나이트, 마법사-전체 전직,
                마법사-매지션, 마법사-위자드(불,독), 마법사-위자드(썬,콜), 마법사-클레릭, 마법사-메이지(불,독),
                마법사-메이지(썬,콜), 마법사-프리스트, 마법사-아크메이지(불,독), 마법사-아크메이지(썬,콜), 마법사-비숍,
                궁수-전체 전직, 궁수-아처, 궁수-헌터, 궁수-사수, 궁수-레인저, 궁수-저격수, 궁수-보우마스터, 궁수-신궁,
                궁수-아처(패스파인더), 궁수-에인션트아처, 궁수-체이서, 궁수-패스파인더, 도적-전체 전직, 도적-로그, 도적-어쌔신,
                도적-시프, 도적-허밋, 도적-시프마스터, 도적-나이트로드, 도적-섀도어, 도적-세미듀어러, 도적-듀어러, 도적-듀얼마스터,
                도적-슬래셔, 도적-듀얼블레이더, 해적-전체 전직, 해적-해적, 해적-인파이터, 해적-건슬링거, 해적-캐논슈터,
                해적-버커니어, 해적-발키리, 해적-캐논블래스터, 해적-바이퍼, 해적-캡틴, 해적-캐논마스터, 기사단-전체 전직,
                기사단-노블레스, 기사단-소울마스터, 기사단-플레임위자드, 기사단-윈드브레이커, 기사단-나이트워커, 기사단-스트라이커,
                기사단-미하일, 아란-전체 전직, 에반-전체 전직, 레지스탕스-전체 전직, 레지스탕스-시티즌, 레지스탕스-배틀메이지,
                레지스탕스-와일드헌터, 레지스탕스-메카닉, 레지스탕스-데몬슬레이어, 레지스탕스-데몬어벤져, 레지스탕스-제논,
                레지스탕스-블래스터, 메르세데스-전체 전직, 팬텀-전체 전직, 루미너스-전체 전직, 카이저-전체 전직, 엔젤릭버스터-전체 전직,
                초월자-전체 전직, 초월자-제로, 은월-전체 전직, 프렌즈 월드-전체 전직, 프렌즈 월드-키네시스, 카데나-전체 전직,
                일리움-전체 전직, 아크-전체 전직, 호영-전체 전직, 아델-전체 전직, 카인-전체 전직, 라라-전체 전직, 칼리-전체 전직
        page_number (int) : 페이지 번호
        difficulty_level (int): 구간 (0:일반, 1:통달)
        date (datetime): 조회 기준일(KST)

    Returns:
        DojangRanking: 무릉도장 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    return get_dojang_ranking_by_id(
        world_name=world_name,
        job_class=job_class,
        page_number=page_number,
        difficulty_level=difficulty_level,
        date=date,
    )


def get_job_class_dojang_ranking(
    job_class: JobClass,
    page_number: int = 1,
    difficulty_level: int | DojangDifficultyEnum = DojangDifficultyEnum.통달,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> DojangRanking:
    """무릉도장 랭킹 정보를 조회합니다.

    Args:
        job_class (str): 직업 및 전직
            Available values : 초보자-전체 전직, 전사-전체 전직, 전사-검사, 전사-파이터, 전사-페이지, 전사-스피어맨,
                전사-크루세이더, 전사-나이트, 전사-버서커, 전사-히어로, 전사-팔라딘, 전사-다크나이트, 마법사-전체 전직,
                마법사-매지션, 마법사-위자드(불,독), 마법사-위자드(썬,콜), 마법사-클레릭, 마법사-메이지(불,독),
                마법사-메이지(썬,콜), 마법사-프리스트, 마법사-아크메이지(불,독), 마법사-아크메이지(썬,콜), 마법사-비숍,
                궁수-전체 전직, 궁수-아처, 궁수-헌터, 궁수-사수, 궁수-레인저, 궁수-저격수, 궁수-보우마스터, 궁수-신궁,
                궁수-아처(패스파인더), 궁수-에인션트아처, 궁수-체이서, 궁수-패스파인더, 도적-전체 전직, 도적-로그, 도적-어쌔신,
                도적-시프, 도적-허밋, 도적-시프마스터, 도적-나이트로드, 도적-섀도어, 도적-세미듀어러, 도적-듀어러, 도적-듀얼마스터,
                도적-슬래셔, 도적-듀얼블레이더, 해적-전체 전직, 해적-해적, 해적-인파이터, 해적-건슬링거, 해적-캐논슈터,
                해적-버커니어, 해적-발키리, 해적-캐논블래스터, 해적-바이퍼, 해적-캡틴, 해적-캐논마스터, 기사단-전체 전직,
                기사단-노블레스, 기사단-소울마스터, 기사단-플레임위자드, 기사단-윈드브레이커, 기사단-나이트워커, 기사단-스트라이커,
                기사단-미하일, 아란-전체 전직, 에반-전체 전직, 레지스탕스-전체 전직, 레지스탕스-시티즌, 레지스탕스-배틀메이지,
                레지스탕스-와일드헌터, 레지스탕스-메카닉, 레지스탕스-데몬슬레이어, 레지스탕스-데몬어벤져, 레지스탕스-제논,
                레지스탕스-블래스터, 메르세데스-전체 전직, 팬텀-전체 전직, 루미너스-전체 전직, 카이저-전체 전직, 엔젤릭버스터-전체 전직,
                초월자-전체 전직, 초월자-제로, 은월-전체 전직, 프렌즈 월드-전체 전직, 프렌즈 월드-키네시스, 카데나-전체 전직,
                일리움-전체 전직, 아크-전체 전직, 호영-전체 전직, 아델-전체 전직, 카인-전체 전직, 라라-전체 전직, 칼리-전체 전직
        page_number (int) : 페이지 번호
        difficulty_level (int): 구간 (0:일반, 1:통달)
        date (datetime): 조회 기준일(KST)

    Returns:
        DojangRanking: 무릉도장 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """

    return get_dojang_ranking_by_id(
        job_class=job_class,
        page_number=page_number,
        difficulty_level=difficulty_level,
        date=date,
    )


def get_character_dojang_rank(
    character_name: str,
    difficulty_level: int | DojangDifficultyEnum = DojangDifficultyEnum.통달,
    date: kst.KSTAwareDatetime = kst.yesterday(),
) -> DojangRankingInfo | None:
    """무릉도장 랭킹 정보를 조회합니다.

    Args:
        character_name (str): 캐릭터명
        difficulty_level (int): 구간 (0:일반, 1:통달)
        date (datetime): 조회 기준일(KST)

    Returns:
        DojangRankingInfo: 무릉도장 랭킹 정보

    Note:
        - 2023년 12월 22일 데이터부터 조회할 수 있습니다.
        - 오전 8시 30분부터 오늘의 랭킹 정보를 조회할 수 있습니다.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
    """
    """
    Retrieves the ranking information for a character in the Dojang (training ground) in the game MapleStory.

    Args:
        character_name (str): The name of the character for which to retrieve the Dojang ranking information.
        difficulty_level (int | DojangDifficultyEnum): The difficulty level of the Dojang. It can be specified as an integer (0 for novice, 1 for master) or using the DojangDifficultyEnum enumeration (DojangDifficultyEnum.일반 for novice, DojangDifficultyEnum.통달 for master). The default value is DojangDifficultyEnum.통달.
        date (kst.KSTAwareDatetime): The date for which to retrieve the Dojang ranking information. It should be a KST-aware datetime object. The default value is kst.yesterday(), which represents yesterday's date in the KST timezone.

    Returns:
        DojangRankingInfo | None: The Dojang ranking information for the specified character, difficulty level, and date. If the ranking information is found, it returns a DojangRankingInfo object. If no ranking information is found, it returns None.
    """
    ranking = get_dojang_ranking(
        character_name=character_name, difficulty_level=difficulty_level, date=date
    )

    return ranking[0] if len(ranking) == 1 else None
