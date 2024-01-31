from datetime import datetime

from PIL import Image
from pydantic import BaseModel, ConfigDict, Field, computed_field

from maplestory.services.guild import Guild
from maplestory.utils.image import get_image_from_url


class CharacterBasic(BaseModel):
    """캐릭터 기본 정보

    Attributes:
        date (datetime): 조회 기준일 (KST, 일 단위 데이터로 시, 분은 일괄 0으로 표기)
        name (str): 캐릭터 명
        world (str): 월드 명
        gender (str): 캐릭터 성별
        class (str): 캐릭터 직업
        class_level (int): 캐릭터 직업 차수
        level (int): 캐릭터 레벨
        exp (int): 현재 레벨에서 보유한 경험치
        exp_rate (str): 현재 레벨에서 경험치 퍼센트
        guild_name (str | None): 캐릭터 소속 길드 명
        image (str): 캐릭터 외형 이미지
    """

    date: datetime = Field(repr=False)
    name: str = Field(alias="character_name")
    world: str = Field(alias="world_name")
    gender: str = Field(alias="character_gender")
    job: str = Field(alias="character_class")
    job_level: int = Field(alias="character_class_level")
    level: int = Field(alias="character_level")
    exp: int = Field(alias="character_exp")
    exp_rate: float = Field(alias="character_exp_rate")
    guild_name: str | None = Field(alias="character_guild_name")
    image_url: str = Field(alias="character_image", repr=False)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def exp_str(self) -> str:
        return f"{self.exp}({self.exp_rate})"

    @property
    def guild(self) -> Guild:
        return Guild(name=self.guild_name, world=self.world_name)

    @property
    def 조회기준일(self) -> datetime:
        return self.date

    @property
    def 캐릭터명(self) -> str:
        return self.character_name

    @property
    def 월드명(self) -> str:
        return self.world_name

    @property
    def 캐릭터성별(self) -> str:
        return self.character_gender

    @property
    def 캐릭터직업(self) -> str:
        return self.character_class

    @property
    def 캐릭터직업차수(self) -> int:
        return self.character_class_level

    @property
    def 레벨(self) -> int:
        return self.character_level

    @property
    def 현재레벨경험치(self) -> int:
        return self.character_exp

    @property
    def 현재레벨경험치퍼센트(self) -> str:
        return self.character_exp_rate

    @property
    def 길드(self) -> str:
        return self.character_guild_name

    @computed_field
    def image(self) -> Image.Image:
        return get_image_from_url(self.image_url)

    @property
    def 이미지(self) -> str:
        return self.character_image
