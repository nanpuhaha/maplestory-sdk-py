from rich import print

from maplestory.apis.character import get_character_ability_by_ocid
from maplestory.models.character.ability import Ability
from maplestory.services.character import get_character_ability


def test_get_character_ability_by_ocid(character_ocid: str):
    character_ability = get_character_ability_by_ocid(character_ocid)
    print(character_ability)
    assert isinstance(character_ability, Ability)


def test_get_character_ability(character_name: str):
    character_ability = get_character_ability(character_name)
    print(character_ability)
    assert isinstance(character_ability, Ability)
