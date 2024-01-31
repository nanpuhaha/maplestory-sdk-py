from rich import print

from maplestory.apis.character import get_character_link_skill_by_ocid
from maplestory.models.character.link_skill import CharacterLinkSkill
from maplestory.services.character import get_character_link_skill


def test_get_character_link_skill_by_ocid(character_ocid: str):
    character_link_skill = get_character_link_skill_by_ocid(character_ocid)
    print(character_link_skill)
    assert isinstance(character_link_skill, CharacterLinkSkill)


def test_get_character_link_skill(character_name: str):
    character_link_skill = get_character_link_skill(character_name)
    print(character_link_skill)
    assert isinstance(character_link_skill, CharacterLinkSkill)
