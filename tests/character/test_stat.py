from rich import print

from maplestory.apis.character import get_character_stat_by_ocid
from maplestory.models.character.stat import CharacterStat
from maplestory.services.character import get_character_stat


def test_get_character_stat_by_ocid(character_ocid: str):
    character_stat = get_character_stat_by_ocid(character_ocid)
    print(character_stat)
    assert isinstance(character_stat, CharacterStat)


def test_get_character_stat(character_name: str):
    character_stat = get_character_stat(character_name)
    print(character_stat)
    assert isinstance(character_stat, CharacterStat)
