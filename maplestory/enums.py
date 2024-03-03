from enum import Enum

import maplestory.utils.kst as kst


class BaseEnum(Enum):
    """확장된 Enum 클래스로 키와 값에 대한 메서드를 제공합니다."""

    @classmethod
    def keys(cls) -> list[str]:
        """Enum 클래스의 모든 키를 리스트로 반환합니다.

        Returns:
            list: Enum 클래스의 모든 키를 포함하는 리스트입니다.
        """

        return list(cls.__members__)

    @classmethod
    def values(cls) -> list:
        """Enum 클래스의 모든 값을 리스트로 반환합니다.

        Returns:
            list: Enum 클래스의 모든 값을 포함하는 리스트입니다.
        """

        return [c.value for c in cls]

    @classmethod
    def members(cls) -> dict:
        """Enum 클래스의 모든 값을 리스트로 반환합니다.

        Returns:
            dict: Enum 클래스의 모든 값을 포함하는 리스트입니다.
        """

        return {k: v.value for k, v in cls._member_map_.items()}


class Grade(BaseEnum):
    LEGENDARY = "레전드리"
    UNIQUE = "유니크"
    EPIC = "에픽"
    RARE = "레어"


class WorldTypeEnum(BaseEnum):
    """게임 내의 월드 타입을 나타내는 Enum 클래스입니다."""

    NORMAL = 0
    REBOOT = 1

    일반 = 0
    리부트 = 1


class NormalWorld(BaseEnum):
    SCANIA = "스카니아"
    BERA = "베라"
    LUNA = "루나"
    ZENITH = "제니스"
    CROA = "크로아"
    UNION = "유니온"
    ELYSIUM = "엘리시움"
    ENOSIS = "이노시스"
    RED = "레드"
    AURORA = "오로라"
    ARCANE = "아케인"
    NOVA = "노바"
    BURNING = "버닝"
    BURNING2 = "버닝2"
    BURNING3 = "버닝3"


class RebootWorld(BaseEnum):
    REBOOT = "리부트"
    REBOOT2 = "리부트2"


World = BaseEnum("World", {**NormalWorld.members(), **RebootWorld.members()})


class GuildRankTypeEnum(BaseEnum):
    """길드 랭킹 타입을 나타내는 Enum 클래스입니다."""

    WEEKLY_FAME = 0
    FLAG_RACE = 1
    SEWER = 2

    주간명성치 = 0
    플래그레이스 = 1
    지하수로 = 2


class DojangDifficultyEnum(BaseEnum):
    """무릉도장 구간를 나타내는 Enum 클래스입니다."""

    NOVICE = 0
    MASTER = 1

    일반 = 0  # 105 ~ 200 레벨 (입문?)
    통달 = 1  # 201 이상 레벨


class QueryableDateEnum(BaseEnum):
    """각 카테고리별 조회 가능한 최소 날짜를 나타내는 Enum 클래스입니다."""

    CHARACTER = kst.datetime(2023, 12, 21)
    UNION = kst.datetime(2023, 12, 21)
    GUILD = kst.datetime(2023, 12, 21)
    RANKING = kst.datetime(2023, 12, 22)
    CUBE = kst.datetime(2022, 11, 25)
    STARFORCE = kst.datetime(2023, 12, 27)
    POTENTIAL = kst.datetime(2024, 1, 25)

    캐릭터 = kst.datetime(2023, 12, 21)
    유니온 = kst.datetime(2023, 12, 21)
    길드 = kst.datetime(2023, 12, 21)
    랭킹 = kst.datetime(2023, 12, 22)
    큐브 = kst.datetime(2022, 11, 25)
    스타포스 = kst.datetime(2023, 12, 27)
    잠재능력 = kst.datetime(2024, 1, 25)
