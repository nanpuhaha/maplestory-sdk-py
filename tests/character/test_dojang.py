from rich import print

from maplestory.apis.character import get_character_dojang_record_by_ocid
from maplestory.models.character.dojang import CharacterDojang
from maplestory.services.character import get_character_dojang_record


def test_get_character_dojang_record_by_ocid(character_ocid: str):
    character_dojang_record = get_character_dojang_record_by_ocid(character_ocid)
    print(character_dojang_record)
    assert isinstance(character_dojang_record, CharacterDojang)


def test_get_character_dojang_record(character_name: str):
    character_dojang_record = get_character_dojang_record(character_name)
    print(character_dojang_record)
    assert isinstance(character_dojang_record, CharacterDojang)
