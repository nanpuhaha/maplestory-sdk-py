from rich import print

from maplestory.apis.union import (
    get_union_artifact_info_by_ocid,
    get_union_info_by_ocid,
    get_union_raider_info_by_ocid,
)
from maplestory.models.union.artifact import UnionArtifact
from maplestory.models.union.raider import UnionRaider
from maplestory.models.union.union import UnionInfo
from maplestory.services.union import (
    get_union_artifact_info,
    get_union_info,
    get_union_raider_info,
)


def test_get_union_info_by_ocid(character_ocid: str):
    result = get_union_info_by_ocid(character_ocid)
    print(result)
    assert isinstance(result, UnionInfo)


def test_get_union_info(character_name: str):
    result = get_union_info(character_name)
    print(result)
    assert isinstance(result, UnionInfo)


def test_get_union_raider_info_by_ocid(character_ocid: str):
    result = get_union_raider_info_by_ocid(character_ocid)
    print(result)
    assert isinstance(result, UnionRaider)


def test_get_union_raider_info(character_name: str):
    result = get_union_raider_info(character_name)
    print(result)
    assert isinstance(result, UnionRaider)


def test_get_union_artifact_info_by_ocid(character_ocid: str):
    result = get_union_artifact_info_by_ocid(character_ocid)
    print(result)
    assert isinstance(result, UnionArtifact)


def test_get_union_artifact_info(character_name: str):
    result = get_union_artifact_info(character_name)
    print(result)
    assert isinstance(result, UnionArtifact)
