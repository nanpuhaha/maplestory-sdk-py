from rich import print

from maplestory.apis.character import get_character_equipment_by_ocid
from maplestory.models.character.item_equip import CharacterEquipment
from maplestory.services.character import get_character_equipment


def test_get_character_equipment_by_ocid(character_ocid: str):
    character_item_equipment = get_character_equipment_by_ocid(character_ocid)
    print(character_item_equipment)
    assert isinstance(character_item_equipment, CharacterEquipment)


def test_get_character_equipment(character_name: str):
    character_item_equipment = get_character_equipment(character_name)
    print(character_item_equipment)
    assert isinstance(character_item_equipment, CharacterEquipment)
