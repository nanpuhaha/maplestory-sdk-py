from rich import print

from maplestory.apis.character import get_character_beauty_equipment_by_ocid
from maplestory.models.character.beauty_equip import BeautyEquipment
from maplestory.services.character import get_character_beauty_equipment


def test_get_character_beauty_equipment_by_ocid(character_ocid: str):
    character_beauty_equipment = get_character_beauty_equipment_by_ocid(character_ocid)
    print(character_beauty_equipment)
    assert isinstance(character_beauty_equipment, BeautyEquipment)


def test_get_character_beauty_equipment(character_name: str):
    character_beauty_equipment = get_character_beauty_equipment(character_name)
    print(character_beauty_equipment)
    assert isinstance(character_beauty_equipment, BeautyEquipment)
