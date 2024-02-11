from rich import print

from maplestory.apis.character import get_character_android_equipment_by_ocid
from maplestory.models.character.android_equip import AndroidEquipment
from maplestory.services.character import get_character_android_equipment


def test_get_character_android_equipment_by_ocid(character_ocid: str):
    character_android_equipment = get_character_android_equipment_by_ocid(
        character_ocid
    )
    print(character_android_equipment)
    assert isinstance(character_android_equipment, AndroidEquipment)


def test_get_character_android_equipment(character_name: str):
    character_android_equipment = get_character_android_equipment(character_name)
    print(character_android_equipment)
    assert isinstance(character_android_equipment, AndroidEquipment)
