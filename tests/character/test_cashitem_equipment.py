from rich import print

from maplestory.apis.character import get_character_cashitem_equipment_by_ocid
from maplestory.models.character.cashitem_equip import CashitemEquipment
from maplestory.services.character import get_character_cashitem_equipment


def test_get_character_cashitem_equipment_by_ocid(character_ocid: str):
    character_cashitem_equipment = get_character_cashitem_equipment_by_ocid(
        character_ocid
    )
    print(character_cashitem_equipment)
    assert isinstance(character_cashitem_equipment, CashitemEquipment)


def test_get_character_cashitem_equipment(character_name: str):
    character_cashitem_equipment = get_character_cashitem_equipment(character_name)
    print(character_cashitem_equipment)
    assert isinstance(character_cashitem_equipment, CashitemEquipment)
