from datetime import datetime

from PIL import Image
from pydantic import BaseModel, ConfigDict, Field, computed_field

from maplestory.apis.guild import get_basic_info_by_id, get_guild_id
from maplestory.models.guild import GuildBasic
from maplestory.models.guild.basic import GuildSkill
from maplestory.utils.image import get_image_from_base64str, get_image_from_url
from maplestory.utils.kst import yesterday
from maplestory.utils.number import korean_format_number


class Guild(BaseModel):
    name: str = Field(frozen=True)
    world: str = Field(frozen=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @computed_field
    @property
    def id(self) -> str:
        return get_guild_id(self.name, self.world)

    @property
    def oguild_id(self) -> str:
        return self.id

    @computed_field(repr=False)
    @property
    def basic(self) -> GuildBasic:
        return get_basic_info(self.name, self.world)

    @computed_field
    @property
    def level(self) -> int:
        return self.basic.level

    @computed_field
    @property
    def point(self) -> int:
        return self.basic.point

    @computed_field
    @property
    def point_str(self) -> str:
        return korean_format_number(self.point)

    @computed_field
    @property
    def fame(self) -> int:
        return self.basic.fame

    @computed_field
    @property
    def fame_str(self) -> str:
        return korean_format_number(self.fame)

    @computed_field
    @property
    def member_count(self) -> int:
        return self.basic.member_count

    @computed_field
    @property
    def member_names(self) -> list[str]:
        return self.basic.members

    @computed_field
    @property
    def master_name(self) -> str:
        return self.basic.master_name

    @computed_field
    @property
    def skills(self) -> list[GuildSkill]:
        return self.basic.skills

    @computed_field
    @property
    def noblesse_skills(self) -> list[GuildSkill]:
        return self.basic.noblesse_skills

    @computed_field
    @property
    def mark(self) -> Image.Image | None:
        if self.basic.mark:
            return get_image_from_url(self.basic.mark)
        elif self.basic.custom_mark:
            return get_image_from_base64str(self.basic.custom_mark)
        return None

    @computed_field
    @property
    def is_custom_mark(self) -> bool:
        return self.basic.custom_mark is not None


def get_basic_info(
    guild_name: str,
    world_name: str,
    date: datetime = yesterday(),
) -> GuildBasic:
    """
    길드 기본 정보를 조회합니다.
    Fetches the basic information of the guild.

    Args:
        guild_name : 길드 명. The name of the guild.
        world_name : 월드 명. The name of the world.
        date : 조회 기준일(KST). Reference date for the query (KST).

    Returns:
        GuildBasic: 길드의 기본 정보. The basic information of the guild.
    """

    guild_id = get_guild_id(guild_name, world_name)
    return get_basic_info_by_id(guild_id, date)
