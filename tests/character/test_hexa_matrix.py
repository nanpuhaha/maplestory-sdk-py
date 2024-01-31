from rich import print

from maplestory.apis.character import (
    get_character_hexamatrix_by_ocid,
    get_character_hexamatrix_stat_by_ocid,
)
from maplestory.models.character.hexamatrix import HexaMatrix
from maplestory.models.character.hexamatrix_stat import HexaMatrixStat
from maplestory.services.character import (
    get_character_hexamatrix,
    get_character_hexamatrix_stat,
)

# NOTE: HEXA 코어 정보가 없는 경우 None으로 표기됩니다.
# response = {'date': '2024-01-19T00:00+09:00', 'character_hexa_core_equipment': None}


def test_get_character_hexamatrix_by_ocid(character_ocid: str):
    character_hexamatrix = get_character_hexamatrix_by_ocid(character_ocid)
    print(character_hexamatrix)
    assert isinstance(character_hexamatrix, HexaMatrix)


def test_get_character_hexamatrix_stat_by_ocid(character_ocid: str):
    character_hexamatrix_stat = get_character_hexamatrix_stat_by_ocid(character_ocid)
    print(character_hexamatrix_stat)
    assert isinstance(character_hexamatrix_stat, HexaMatrixStat)


def test_get_character_hexamatrix(character_name: str):
    character_hexamatrix = get_character_hexamatrix(character_name)
    print(character_hexamatrix)
    assert isinstance(character_hexamatrix, HexaMatrix)


def test_get_character_hexamatrix_stat(character_name: str):
    character_hexamatrix_stat = get_character_hexamatrix_stat(character_name)
    print(character_hexamatrix_stat)
    assert isinstance(character_hexamatrix_stat, HexaMatrixStat)
