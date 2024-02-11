from rich import print

from maplestory.apis.character import get_popularity_by_ocid
from maplestory.models.character.popularity import Popularity
from maplestory.services.character import get_popularity


def test_get_popularity_by_ocid(character_ocid: str):
    character_popularity = get_popularity_by_ocid(character_ocid)
    print(character_popularity)
    assert isinstance(character_popularity, Popularity)


def test_get_popularity(character_name: str):
    character_popularity = get_popularity(character_name)
    print(character_popularity)
    assert isinstance(character_popularity, Popularity)
