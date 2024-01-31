from rich import print

from maplestory.apis.character import get_character_symbol_equipment_by_ocid
from maplestory.models.character.symbol_equip import SymbolEquipment
from maplestory.services.character import get_character_symbol_equipment


def test_get_character_symbol_equipment_by_ocid(character_ocid: str):
    character_symbol_equipment = get_character_symbol_equipment_by_ocid(character_ocid)
    print(character_symbol_equipment)
    assert isinstance(character_symbol_equipment, SymbolEquipment)


def test_get_character_symbol_equipment(character_name: str):
    character_symbol_equipment = get_character_symbol_equipment(character_name)
    print(character_symbol_equipment)
    assert isinstance(character_symbol_equipment, SymbolEquipment)
