from rich import print

from maplestory.apis.character import get_character_skill_by_ocid
from maplestory.models.character.skill import CharacterSkill
from maplestory.services.character import get_character_skill


def test_get_character_skill_by_ocid(character_ocid: str, skill_grade: int):
    character_skill = get_character_skill_by_ocid(character_ocid, skill_grade)
    print(character_skill)
    assert isinstance(character_skill, CharacterSkill)
    assert isinstance(character_skill.character_skill_grade, int)
    assert character_skill.character_skill_grade == skill_grade


def test_get_character_skill(character_name: str, skill_grade: int):
    character_skill = get_character_skill(character_name, skill_grade)
    print(character_skill)
    assert isinstance(character_skill, CharacterSkill)
    assert isinstance(character_skill.character_skill_grade, int)
    assert character_skill.character_skill_grade == skill_grade
