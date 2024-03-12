from typing import get_args

from pydantic import BaseModel, Field, field_validator

from maplestory.types.character import Classes, SkillGrade
from maplestory.utils.kst import KSTAwareDatetime


class CharacterSkillInfo(BaseModel):
    """스킬 정보

    Attributes:
        name (str): 스킬 명
        description (str): 스킬 설명
        level (int): 스킬 레벨
        effect (str | None): 스킬 레벨 별 효과 설명
        icon (str): 스킬 아이콘
    """

    name: str = Field(alias="skill_name")
    description: str = Field(alias="skill_description")
    level: int = Field(alias="skill_level")
    effect: str | None = Field(alias="skill_effect")
    icon: str = Field(alias="skill_icon")


class CharacterSkill(BaseModel):
    """캐릭터 스킬 정보

    Attributes:
        date (KSTAwareDatetime): 조회 기준일 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        character_class (str): 캐릭터 직업
        grade (int): 스킬 전직 차수
        skills (list[CharacterSkillInfo]): 스킬 정보
    """

    date: KSTAwareDatetime = Field(repr=False)
    character_class: Classes
    grade: SkillGrade = Field(alias="character_skill_grade")
    skills: list[CharacterSkillInfo] = Field(alias="character_skill")

    @field_validator("character_class", mode="before")
    @classmethod
    def is_valid_job_class(cls, v: str) -> str:
        if v in get_args(Classes):
            return v

        raise ValueError(f"character_class must be in {get_args(Classes)}.")
