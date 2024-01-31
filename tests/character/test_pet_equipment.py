from rich import print

from maplestory.apis.character import get_character_pet_equipment_by_ocid
from maplestory.models.character.pet_equip import CharacterPet
from maplestory.services.character import get_character_pet_equipment


def test_get_character_pet_equipment_by_ocid(character_ocid: str):
    character_pet_equipment = get_character_pet_equipment_by_ocid(character_ocid)
    print(character_pet_equipment)
    assert isinstance(character_pet_equipment, CharacterPet)


def test_get_character_pet_equipment(character_name: str):
    character_pet_equipment = get_character_pet_equipment(character_name)
    print(character_pet_equipment)
    assert isinstance(character_pet_equipment, CharacterPet)
