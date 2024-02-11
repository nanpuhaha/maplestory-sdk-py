from rich import print

from maplestory.apis.character import get_character_set_effect_by_ocid
from maplestory.models.character.set_effect import SetEffect
from maplestory.services.character import get_character_set_effect


def test_get_character_set_effect_by_ocid(character_ocid: str):
    character_set_effect = get_character_set_effect_by_ocid(character_ocid)
    print(character_set_effect)
    assert isinstance(character_set_effect, SetEffect)


def test_get_character_set_effect(character_name: str):
    character_set_effect = get_character_set_effect(character_name)
    print(character_set_effect)
    assert isinstance(character_set_effect, SetEffect)
