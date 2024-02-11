from rich import print

from maplestory.apis.character import get_character_propensity_by_ocid
from maplestory.models.character.propensity import Propensity
from maplestory.services.character import get_character_propensity


def test_get_character_propensity_by_ocid(character_ocid: str):
    character_propensity = get_character_propensity_by_ocid(character_ocid)
    print(character_propensity)
    assert isinstance(character_propensity, Propensity)


def test_get_character_propensity(character_name: str):
    character_propensity = get_character_propensity(character_name)
    print(character_propensity)
    assert isinstance(character_propensity, Propensity)
