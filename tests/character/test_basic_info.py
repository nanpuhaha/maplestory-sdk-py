from rich import print

from maplestory.apis.character import get_basic_character_info_by_ocid
from maplestory.models.character.basic import CharacterBasic
from maplestory.services.character import get_basic_character_info


def test_get_basic_character_info_by_ocid(character_ocid: str):
    character_basic = get_basic_character_info_by_ocid(character_ocid)
    print(character_basic)
    assert isinstance(character_basic, CharacterBasic)


def test_get_basic_character_info(character_name: str):
    character_basic = get_basic_character_info(character_name)
    print(character_basic)
    assert isinstance(character_basic, CharacterBasic)
