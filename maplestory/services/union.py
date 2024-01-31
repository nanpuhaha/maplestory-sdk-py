"""
이 모듈은 메이플스토리 게임의 유니온 정보를 가져오고 처리하는 함수를 제공합니다.
This module provides functions to fetch and handle Union information in the MapleStory game.

이 모듈에는 주어진 캐릭터 식별자(ocid)와 참조 날짜에 대한 유니온 레벨과 유니온 등급 정보를 가져오는 `get_union_info` 함수가 포함되어 있습니다.
It includes a function `get_union_info` which fetches the Union level and Union rank information
for a given character identifier (ocid) and reference date.

이 모듈은 `maplestory.models.union` 패키지의 `Union`과 `UnionRaider` 모델과 `maplestory.utils.date`와 `maplestory.utils.network` 패키지의 유틸리티 함수를 사용합니다.
The module uses the `Union` and `UnionRaider` models from the `maplestory.models.union` package
and utility functions from the `maplestory.utils.date` and `maplestory.utils.network` packages.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Generator

from pydantic import BaseModel, RootModel, computed_field, field_validator

from maplestory.apis.union import (
    get_union_artifact_info_by_ocid,
    get_union_info_by_ocid,
    get_union_raider_info_by_ocid,
)
from maplestory.models.union import UnionArtifact, UnionInfo, UnionRaider
from maplestory.models.union.artifact import UnionArtifactEffect
from maplestory.services.character import get_character_id
from maplestory.utils.kst import yesterday


class Union(BaseModel):
    character_name: str
    date: datetime = yesterday()

    @computed_field(repr=False)
    @property
    def union_info(self) -> UnionInfo:
        return get_union_info(self.character_name, self.date)

    @computed_field
    @property
    def level(self) -> int:
        return self.union_info.level

    @computed_field
    @property
    def grade(self) -> str:
        return self.union_info.grade

    @computed_field(repr=False)
    @property
    def raider_info(self) -> UnionRaider:
        return get_union_raider_info(self.character_name, self.date)

    @computed_field
    @property
    def raider_stats(self) -> UnionStats:
        stats = UnionStats.parse_list(self.raider_info.raider_stats)
        return stats.summarize(split_multiple=True)

    @property
    def 공격대원효과(self) -> UnionStats:
        return self.raider_stats

    @computed_field
    @property
    def occupied_stats(self) -> UnionStats:
        stats = UnionStats.parse_list(self.raider_info.occupied_stats)
        return stats.summarize(split_multiple=True)

    @property
    def 공격대점령효과(self) -> UnionStats:
        return self.occupied_stats

    @computed_field(repr=False)
    @property
    def artifact(self) -> UnionArtifact:
        return get_union_artifact_info(self.character_name, self.date)

    @computed_field
    @property
    def artifact_effects(self) -> list[UnionArtifactEffect]:
        return self.artifact.effects

    @property
    def 아티팩트효과(self) -> list[UnionArtifactEffect]:
        return self.artifact_effects


def get_union_info(
    character_name: str,
    date: datetime = yesterday(),
) -> UnionInfo:
    """
    유니온 레벨 및 유니온 등급 정보를 조회합니다.
    Fetches the Union level and Union rank information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date: 조회 기준일 (KST).
                        Reference date for the query (KST).

    Returns:
        Union: 유니온의 레벨 및 등급 정보.
               The level and rank information of the Union.
    """

    character_ocid = get_character_id(character_name)
    return get_union_info_by_ocid(character_ocid, date)


def get_union_raider_info(
    character_name: str,
    date: datetime = yesterday(),
) -> UnionRaider:
    """
    유니온에 배치된 공격대원 효과 및 공격대 점령 효과 등 상세 정보를 조회합니다.
    Fetches the detailed information of the effect of the attack members placed in the Union and the effect of the attack occupation.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date: 조회 기준일 (KST).
              Reference date for the query (KST).

    Returns:
        UnionRaider: 유니온에 배치된 공격대원 효과 및 공격대 점령 효과 등의 상세 정보.
                     The detailed information of the effect of the attack members placed in the Union and the effect of the attack occupation.
    """

    character_ocid = get_character_id(character_name)
    return get_union_raider_info_by_ocid(character_ocid, date)


def summarize_union_stat(stat: str) -> dict[str, str]:
    if m := re.search(
        r"(?P<name>.+) (?P<value>\d+(\.\d+)?)(?P<percent>%?) (?P<updown>.+)", stat
    ):
        return m.groupdict()

    raise ValueError("Invalid stat format.")


class UnionStat(BaseModel):
    stat: str

    @field_validator("stat", mode="before")
    @classmethod
    def unify_format(cls, stat: str) -> str:
        # '공격력 20, 마력 20 증가' -> '공격력/마력 20 증가'
        pattern = r"(\w+) (\d+), (\w+) (\d+) (\w+)"
        if m := re.match(pattern, stat):
            if m[2] == m[4]:
                replacement = r"\1/\3 \2 \5"
                return re.sub(pattern, replacement, stat)

        # '몬스터 방어율 무시 20% 증가' -> '방어율 무시 20% 증가'
        if "몬스터 방어율 무시" in stat:
            stat = stat.replace("몬스터 ", "")

        return stat

    @computed_field(repr=False)
    @property
    def parsed_stat(self) -> dict[str, str]:
        return summarize_union_stat(self.stat)

    @computed_field(repr=False)
    @property
    def name(self) -> str:
        return self.parsed_stat.get("name")

    @property
    def is_multi_name(self) -> bool:
        return "," in self.name or "/" in self.name

    @property
    def multi_name(self) -> str | None:
        if "," in self.name:
            # 'STR, DEX, LUK 40 증가'
            return [s.strip() for s in self.name.split(",")]
        elif "/" in self.name:
            # '공격력/마력 20 증가'
            return [s.strip() for s in self.name.split("/")]
        return None

    @computed_field(repr=False)
    @property
    def percent(self) -> str:
        return self.parsed_stat.get("percent")

    @computed_field(repr=False)
    @property
    def is_percent(self) -> bool:
        return self.percent == "%"

    @computed_field(repr=False)
    @property
    def value(self) -> int | float:
        try:
            return int(self.parsed_stat.get("value"))
        except ValueError:
            return float(self.parsed_stat.get("value"))

    @computed_field(repr=False)
    @property
    def updown(self) -> str:
        return self.parsed_stat.get("updown")

    def __add__(self, other: UnionStat) -> UnionStat:
        if self.name != other.name:
            raise ValueError("Cannot add different stats.")
        if self.updown != other.updown:
            raise ValueError("Cannot add stats with different updown.")
        if self.is_percent != other.is_percent:
            raise ValueError(
                "Cannot add stats with different types (percent vs number)."
            )

        new_value = self.value + other.value
        if self.is_percent:
            new_value = f"{new_value}%"
        return UnionStat(stat=f"{self.name} {new_value} {self.updown}")

    def __radd__(self, other: UnionStat) -> UnionStat:
        if other == 0:
            return self
        return self.__add__(other) if isinstance(other, UnionStat) else NotImplemented


class UnionStats(RootModel):
    root: list[UnionStat]

    def __repr__(self) -> str:
        return f"UnionStats({self.root!r})"

    def __rich_repr__(self) -> Generator:
        yield self.root

    def model_post_init(self, __context: Any) -> None:
        """
        모델 생성 후 초기화를 수행합니다. 스탯의 이름을 기준으로 root를 정렬합니다.

        Args:
            __context (Any): 초기화 후의 컨텍스트.
        """
        """
        Initializes the model post creation. Sorts the root based on the name of the stat.

        Args:
            __context (Any): The context for post initialization.
        """

        self.root = sorted(self.root, key=lambda x: x.name)

    def group_stats(self, split_multiple: bool = False) -> dict[str, list[UnionStat]]:
        """
        스탯의 이름과 퍼센트 여부를 기준으로 스탯을 그룹화합니다.
        split_multiple이 True인 경우, 다중 이름 스탯을 개별 스탯으로 분리합니다.

        Args:
            split_multiple (bool): 다중 이름 스탯을 분리할지 여부. 기본값은 False입니다.

        Returns:
            Dict[str, List[UnionStat]]: 그룹화된 스탯.
        """
        """
        Groups the stats based on the name and whether it is a percentage.
        If split_multiple is True, splits the multi-name stats into individual stats.

        Args:
            split_multiple (bool): Whether to split multi-name stats. Default is False.

        Returns:
            Dict[str, List[UnionStat]]: The grouped stats.
        """
        stats = []
        if split_multiple:
            for stat in self.root:
                if stat.is_multi_name:
                    stats.extend(
                        [
                            UnionStat(
                                stat=f"{name} {stat.value}{stat.percent} {stat.updown}"
                            )
                            for name in stat.multi_name
                        ]
                    )
                else:
                    stats.append(stat)
        else:
            stats = self.root

        return {
            (stat.name, stat.is_percent): [
                s
                for s in stats
                if s.name == stat.name and s.is_percent == stat.is_percent
            ]
            for stat in stats
        }

    def group_with_split_multiple(self) -> dict[str, list[UnionStat]]:
        """
        split_multiple을 True로 설정하여 스탯을 그룹화합니다.

        Returns:
            Dict[str, List[UnionStat]]: 그룹화된 스탯.
        """
        """
        Groups the stats with split_multiple set to True.

        Returns:
            Dict[str, List[UnionStat]]: The grouped stats.
        """
        return self.group_stats(split_multiple=True)

    @classmethod
    def parse_list(cls, data: list[str]) -> UnionStats:
        """
        스탯의 리스트를 파싱하여 UnionStats 객체를 생성합니다.

        Args:
            data (List[str]): 스탯의 리스트.

        Returns:
            UnionStats: 생성된 UnionStats 객체.
        """
        """
        Parses a list of stats and creates a UnionStats object.

        Args:
            data (List[str]): The list of stats.

        Returns:
            UnionStats: The created UnionStats object.
        """
        return cls(root=[UnionStat(stat=stat) for stat in data])

    def summarize(self, split_multiple: bool = False) -> UnionStats:
        """
        스탯을 요약합니다. '방어율 무시'는 합이 아닌 곱으로 처리되므로 별도로 처리합니다.

        Args:
            split_multiple (bool): 다중 이름 스탯을 분리할지 여부. 기본값은 False입니다.

        Returns:
            UnionStats: 요약된 스탯.
        """
        """
        Summarizes the stats. '방어율 무시' (Ignore Defense Rate) is handled separately
        as it is not summed but multiplied.

        Args:
            split_multiple (bool): Whether to split multi-name stats. Default is False.

        Returns:
            UnionStats: The summarized stats.
        """
        combined_stats = []
        grouped_stats = self.group_stats(split_multiple)

        for (stat_name, _), stats in grouped_stats.items():
            if stat_name == "방어율 무시":
                # '방어율 무시' (Ignore Defense Rate) is multiplied, not summed
                # 방어율 무시는 합적용이 아니라 곱적용이라 별도로 처리
                combined_stats.extend(stats)
            else:
                combined_stats.append(sum(stats))

        return UnionStats(root=combined_stats)


def get_union_artifact_info(
    character_name: str,
    date: datetime = yesterday(),
) -> UnionArtifact:
    """
    유니온 아티팩트 정보를 조회합니다.
    Fetches the Union Artifact information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date: 조회 기준일 (KST).
                        Reference date for the query (KST).

    Returns:
        UnionArtifact: 유니온 아티팩트 정보.
                       The information of the Union Artifact.
    """

    character_ocid = get_character_id(character_name)
    return get_union_artifact_info_by_ocid(character_ocid, date)
