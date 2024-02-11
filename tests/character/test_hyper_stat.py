from rich import print

from maplestory.apis.character import get_character_hyper_stat_by_ocid
from maplestory.models.character.hyper_stat import HyperStat
from maplestory.services.character import get_character_hyper_stat


def test_get_character_hyper_stat_by_ocid(character_ocid: str):
    character_hyper_stat = get_character_hyper_stat_by_ocid(character_ocid)
    print(character_hyper_stat)
    assert isinstance(character_hyper_stat, HyperStat)


def test_get_character_hyper_stat(character_name: str):
    character_hyper_stat = get_character_hyper_stat(character_name)
    print(character_hyper_stat)
    assert isinstance(character_hyper_stat, HyperStat)
