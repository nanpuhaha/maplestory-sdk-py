import pytest
from rich import print

from maplestory.apis.guild import get_basic_info_by_id, get_guild_id
from maplestory.models.guild.basic import GuildBasic
from maplestory.services.guild import get_basic_info

TEST_GUILDS = [("리더", "스카니아"), ("좋은부자", "엘리시움")]


@pytest.mark.parametrize("guild_name,world_name", TEST_GUILDS)
def test_get_id(guild_name: str, world_name: str):
    guild_id = get_guild_id(guild_name, world_name)
    print(f"{guild_name = }, {world_name = } -> {guild_id = }")
    assert isinstance(guild_id, str)


@pytest.mark.parametrize(
    "guild_id", ["789b457f357ce6ac3e1bfa1c95ccaac6", "604aebb0f9aaaaea871231a0412ec0b3"]
)
def test_get_basic_character_info_by_ocid(guild_id: str):
    result = get_basic_info_by_id(guild_id)
    print(result)
    assert isinstance(result, GuildBasic)


@pytest.mark.parametrize("guild_name,world_name", TEST_GUILDS)
def test_get_basic_info(guild_name: str, world_name: str):
    result = get_basic_info(guild_name, world_name)
    print(result)
    assert isinstance(result, GuildBasic)
