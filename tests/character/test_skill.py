import pytest
from pydantic import ValidationError
from rich import print

from maplestory.apis.character import get_character_skill_by_ocid
from maplestory.models.character.skill import CharacterSkill
from maplestory.services.character import get_character_skill

COMMON_SKILL_DATA = {
    "date": "2024-03-05T00:00+09:00",
    "character_class": "아크메이지(썬,콜)",
    "character_skill": [
        {
            "skill_name": "에너지 볼트",
            "skill_description": "[마스터 레벨 : 20]\r\n적에게 닿으면 폭발하는 에너지 응집체를 발사한다.",
            "skill_level": 20,
            "skill_effect": "MP 24 소비, 최대 4명의 적에게 78%의 데미지로 4번 공격",
            "skill_icon": "https://open.api.nexon.com/static/maplestory/SkillIcon/KFPALHPBMI.png",
        }
    ],
}


def test_get_character_skill_by_ocid(character_ocid: str, skill_grade: str):
    character_skill = get_character_skill_by_ocid(character_ocid, skill_grade)
    print(character_skill)
    assert isinstance(character_skill, CharacterSkill)
    assert isinstance(character_skill.grade, str)
    assert character_skill.grade == skill_grade


def test_get_character_skill(character_name: str, skill_grade: str):
    character_skill = get_character_skill(character_name, skill_grade)
    print(character_skill)
    assert isinstance(character_skill, CharacterSkill)
    assert isinstance(character_skill.grade, str)
    assert character_skill.grade == skill_grade


class TestSkillGradeValidation:

    def test_input_is_valid(self):
        data = {
            **COMMON_SKILL_DATA,
            "character_skill_grade": "1",
        }

        character_skill = CharacterSkill.model_validate(data)
        assert isinstance(character_skill, CharacterSkill)
        assert isinstance(character_skill.grade, str)
        assert character_skill.grade == "1"

    def test_input_is_float(self):
        data = {
            **COMMON_SKILL_DATA,
            "character_skill_grade": 1.5,
        }

        with pytest.raises(ValidationError):
            CharacterSkill.model_validate(data)

    def test_input_is_negative_integer(self):
        data = {
            **COMMON_SKILL_DATA,
            "character_skill_grade": -1,
        }

        with pytest.raises(ValidationError):
            CharacterSkill.model_validate(data)

    def test_input_is_string_representation_of_non_integer(self):
        data = {
            **COMMON_SKILL_DATA,
            "character_skill_grade": "abc",
        }

        with pytest.raises(ValidationError):
            CharacterSkill.model_validate(data)

    def test_input_is_empty_string(self):
        data = {
            **COMMON_SKILL_DATA,
            "character_skill_grade": "",
        }

        with pytest.raises(ValidationError):
            CharacterSkill.model_validate(data)

    def test_input_is_string_representation_of_negative_integer(self):
        data = {
            **COMMON_SKILL_DATA,
            "character_skill_grade": "-1",
        }

        with pytest.raises(ValidationError):
            CharacterSkill.model_validate(data)

    def test_input_is_invalid_integer_greater_than_6(self):
        data = {
            **COMMON_SKILL_DATA,
            "character_skill_grade": "99",
        }

        with pytest.raises(ValidationError):
            CharacterSkill.model_validate(data)

    def test_input_is_string_representation_of_valid_integer_with_whitespaces(self):
        data = {
            **COMMON_SKILL_DATA,
            "character_skill_grade": " 3 ",
        }

        with pytest.raises(ValidationError):
            CharacterSkill.model_validate(data)
