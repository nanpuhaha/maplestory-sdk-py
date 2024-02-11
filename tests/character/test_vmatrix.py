from rich import print

from maplestory.apis.character import get_character_vmatrix_by_ocid
from maplestory.models.character.vmatrix import VMatrix
from maplestory.services.character import get_character_vmatrix


def test_get_character_vmatrix_by_ocid(character_ocid: str):
    character_vmatrix = get_character_vmatrix_by_ocid(character_ocid)
    print(character_vmatrix)
    assert isinstance(character_vmatrix, VMatrix)


def test_get_character_vmatrix(character_name: str):
    character_vmatrix = get_character_vmatrix(character_name)
    print(character_vmatrix)
    assert isinstance(character_vmatrix, VMatrix)
