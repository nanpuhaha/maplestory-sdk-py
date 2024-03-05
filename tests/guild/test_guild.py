from datetime import datetime

import httpx
import pytest
from PIL import Image
from pydantic import ValidationError
from rich import print

from maplestory.apis.guild import get_basic_info_by_id, get_guild_id
from maplestory.error import APIError
from maplestory.models.guild.basic import GuildBasic, GuildSkill
from maplestory.services.guild import Guild, get_basic_info
from maplestory.utils.kst import KST_TZ

TEST_GUILDS = [("리더", "스카니아"), ("좋은부자", "엘리시움")]


class TestGetBasicInfoById:

    # Should return a GuildBasic object when given a valid guild_id and date
    def test_valid_guild_id_and_date(self):
        guild_id = "9c64f32a53218b692a2360b4616fc15c"  # 스카니아 온앤온
        date = datetime(2024, 1, 1)

        result = get_basic_info_by_id(guild_id, date)

        assert isinstance(result, GuildBasic)
        assert isinstance(result.custom_mark_img, Image.Image)

    # Should raise an APIError when the API returns an error message
    def test_invalid_guild_id(self):
        guild_id = "invalid_guild_id"
        date = datetime(2024, 1, 1)

        with pytest.raises(APIError, match="Please input valid id"):
            get_basic_info_by_id(guild_id, date)

    # Should raise an APIError when the API returns an error message
    def test_invalid_date(self):
        guild_id = "9c64f32a53218b692a2360b4616fc15c"  # 스카니아 온앤온
        date = datetime(2023, 12, 10)

        with pytest.raises(ValidationError):
            get_basic_info_by_id(guild_id, date)


@pytest.mark.parametrize("guild_name,world_name", TEST_GUILDS)
def test_get_id(guild_name: str, world_name: str):
    guild_id = get_guild_id(guild_name, world_name)
    print(f"{guild_name = }, {world_name = } -> {guild_id = }")
    assert isinstance(guild_id, str)


@pytest.mark.parametrize(
    "guild_id", ["789b457f357ce6ac3e1bfa1c95ccaac6", "604aebb0f9aaaaea871231a0412ec0b3"]
)
def test_get_basic_info_by_ocid(guild_id: str):
    result = get_basic_info_by_id(guild_id)
    print(result)
    assert isinstance(result, GuildBasic)


@pytest.mark.parametrize("guild_name,world_name", TEST_GUILDS)
def test_get_basic_info(guild_name: str, world_name: str):
    result = get_basic_info(guild_name, world_name)
    print(result)
    assert isinstance(result, GuildBasic)


def custom_side_effect(url, params, headers, *args, **kwargs):
    if "/guild/id" in url:
        return httpx.Response(
            200,
            json={"oguild_id": "9c64f32a53218b692a2360b4616fc15c"},
            request=httpx.Request(
                "GET",
                "https://open.api.nexon.com/maplestory/v1/guild/id",
                params=params,
                headers=headers,
            ),
        )
    elif "/guild/basic" in url:
        return httpx.Response(
            200,
            json={
                "date": "2024-02-21T00:00+09:00",
                "world_name": "스카니아",
                "guild_name": "온앤온",
                "guild_level": 11,
                "guild_fame": 1746490,
                "guild_point": 148947,
                "guild_master_name": "온앤온",
                "guild_member_count": 2,
                "guild_member": ["온앤온", "꽁앤꽁"],
                "guild_skill": [
                    {
                        "skill_name": "길드 정기 지원Ⅰ",
                        "skill_description": "[마스터 레벨 : 4]\r\n매주 공격력과 마력을 올려주는 길드의 축복과 HP과 MP를 모두 회복시켜 주는 G포션을 지급받을 수 있다.\n지급받은 아이템은 해당 주 일요일까지 사용 가능",
                        "skill_level": 4,
                        "skill_effect": "매주 G포션100개, 길드의 축복 20개 지급",
                        "skill_icon": "https://open.api.nexon.com/static/maplestory/SkillIcon/KFGDLHOBMJ.png",
                    },
                ],
                "guild_noblesse_skill": [
                    {
                        "skill_name": "크게 한방",
                        "skill_description": "[마스터 레벨 : 15]\r\n일정 시간 동안 크리티컬 데미지가 일정 비율 증가한다.",
                        "skill_level": 15,
                        "skill_effect": "30분 동안 크리티컬 데미지 30% 증가, 재사용 대기시간 60분",
                        "skill_icon": "https://open.api.nexon.com/static/maplestory/SkillIcon/KFGDLHPBOF.png",
                    }
                ],
                "guild_mark": None,
                "guild_mark_custom": "iVBORw0KGgoAAAANSUhEUgAAABEAAAARCAYAAAA7bUf6AAAAf0lEQVQ4y92Q0Q2AIAxEr40zuIKjORNuhiPgEDUaJYgFbGL88H7oQbhcH/4lKmwjyUyKv4i1ABGB86Hk0QrZP2QXmObFhH8LEeeDpPPpnzZRNQ49KvzQWVpmnjTSNx41EVH8z2nA8RDPBrzYjvGCWEmHZa3XmOTLWyq0wX0rACtmD0XA3MLsTAAAAABJRU5ErkJggg==",
            },
            request=httpx.Request(
                "GET",
                "https://open.api.nexon.com/maplestory/v1/guild/basic",
                params=params,
                headers=headers,
            ),
        )
    else:
        return httpx.Response(
            404,
            request=httpx.Request("GET", url, params=params, headers=headers),
        )


class TestGuild:
    # Guild object can be created with a name and world.
    def test_guild_creation_with_name_and_world(self):
        guild = Guild(name="ExampleGuild", world="Scania")
        assert guild.name == "ExampleGuild"
        assert guild.world == "Scania"

    # Guild object cannot be created without a name or world.
    def test_guild_creation_without_name_or_world(self):
        with pytest.raises(ValidationError):
            _ = Guild(name="ExampleGuild")
        with pytest.raises(ValidationError):
            _ = Guild(world="Scania")

    # Guild object has an id computed field that can be retrieved.
    def test_guild_id_computed_field(self, mocker):
        # Mock the get_guild_id function
        patcher = mocker.patch(
            "httpx.get",
            return_value=httpx.Response(
                200,
                json={"oguild_id": "1234567890"},
            ),
        )

        guild_id = get_guild_id(guild_name="ExampleGuild", world_name="Scania")
        assert guild_id == "1234567890"

        mocker.stop(patcher)

    # Guild object has computed fields for level, point, fame, member_count, member_names, master_name, skills, noblesse_skills, mark, and is_custom_mark.
    def test_computed_fields(self, mocker):
        patcher = mocker.patch("httpx.get", side_effect=custom_side_effect)

        # Create a Guild object
        guild = Guild(name="온앤온", world="스카니아")

        # Test the computed fields
        assert guild.id == "9c64f32a53218b692a2360b4616fc15c"
        assert guild.oguild_id == "9c64f32a53218b692a2360b4616fc15c"
        assert guild.level == 11
        assert guild.point == 148947
        assert guild.point_str == "14만 8947"
        assert guild.fame == 1746490
        assert guild.fame_str == "174만 6490"
        assert guild.member_count == 2
        assert guild.member_names == ["온앤온", "꽁앤꽁"]
        assert guild.master_name == "온앤온"
        assert guild.skills == [
            GuildSkill(
                skill_name="길드 정기 지원Ⅰ",
                skill_description="[마스터 레벨 : 4]\r\n매주 공격력과 마력을 올려주는 길드의 축복과 HP과 MP를 모두 회복시켜 주는 G포션을 지급받을 수 있다.\n지급받은 아이템은 해당 주 일요일까지 사용 가능",
                skill_level=4,
                skill_effect="매주 G포션100개, 길드의 축복 20개 지급",
                skill_icon="https://open.api.nexon.com/static/maplestory/SkillIcon/KFGDLHOBMJ.png",
            )
        ]
        assert guild.noblesse_skills == [
            GuildSkill(
                skill_name="크게 한방",
                skill_description="[마스터 레벨 : 15]\r\n일정 시간 동안 크리티컬 데미지가 일정 비율 증가한다.",
                skill_level=15,
                skill_effect="30분 동안 크리티컬 데미지 30% 증가, 재사용 대기시간 60분",
                skill_icon="https://open.api.nexon.com/static/maplestory/SkillIcon/KFGDLHPBOF.png",
            )
        ]
        assert isinstance(guild.mark, Image.Image)
        assert guild.is_custom_mark is True
        assert guild.basic == get_basic_info("온앤온", "스카니아")

        mocker.stop(patcher)

    # Computed fields return expected data types.
    def test_computed_fields_data_types(self, mocker):
        patcher = mocker.patch("httpx.get", side_effect=custom_side_effect)

        # Create an instance of the Guild class
        guild = Guild(name="ExampleGuild", world="Scania")

        # Test the computed fields
        assert isinstance(guild.id, str)
        assert isinstance(guild.basic, GuildBasic)
        assert isinstance(guild.level, int)
        assert isinstance(guild.point, int)
        assert isinstance(guild.point_str, str)
        assert isinstance(guild.fame, int)
        assert isinstance(guild.fame_str, str)
        assert isinstance(guild.member_count, int)
        assert isinstance(guild.member_names, list)
        assert all(isinstance(member, str) for member in guild.member_names)
        assert isinstance(guild.master_name, str)
        assert isinstance(guild.skills, list)
        assert all(isinstance(skill, GuildSkill) for skill in guild.skills)
        assert isinstance(guild.noblesse_skills, list)
        assert all(isinstance(skill, GuildSkill) for skill in guild.noblesse_skills)
        assert isinstance(guild.mark, (Image.Image, type(None)))
        assert isinstance(guild.is_custom_mark, bool)

        mocker.stop(patcher)

    # Guild object has a basic computed field that returns a GuildBasic object.
    def test_basic_computed_field_returns_GuildBasic_object(self, mocker):
        patcher = mocker.patch("httpx.get", side_effect=custom_side_effect)

        # Create a Guild object
        guild = Guild(name="온앤온", world="스카니아")

        # Assert that the basic computed field returns a GuildBasic object
        assert isinstance(guild.basic, GuildBasic)
        assert guild.basic == get_basic_info("온앤온", "스카니아")
        assert guild.basic.date == datetime(2024, 2, 21, tzinfo=KST_TZ)
        assert guild.basic.world == "스카니아"
        assert guild.basic.name == "온앤온"
        assert guild.basic.level == 11
        assert guild.basic.fame == 1746490
        assert guild.basic.point == 148947
        assert guild.basic.master_name == "온앤온"
        assert guild.basic.member_count == 2
        assert guild.basic.members == ["온앤온", "꽁앤꽁"]
        assert guild.basic.skills == [
            GuildSkill(
                skill_name="길드 정기 지원Ⅰ",
                skill_description="[마스터 레벨 : 4]\r\n매주 공격력과 마력을 올려주는 길드의 축복과 HP과 MP를 모두 회복시켜 주는 G포션을 지급받을 수 있다.\n지급받은 아이템은 해당 주 일요일까지 사용 가능",
                skill_level=4,
                skill_effect="매주 G포션100개, 길드의 축복 20개 지급",
                skill_icon="https://open.api.nexon.com/static/maplestory/SkillIcon/KFGDLHOBMJ.png",
            )
        ]
        assert guild.basic.noblesse_skills == [
            GuildSkill(
                skill_name="크게 한방",
                skill_description="[마스터 레벨 : 15]\r\n일정 시간 동안 크리티컬 데미지가 일정 비율 증가한다.",
                skill_level=15,
                skill_effect="30분 동안 크리티컬 데미지 30% 증가, 재사용 대기시간 60분",
                skill_icon="https://open.api.nexon.com/static/maplestory/SkillIcon/KFGDLHPBOF.png",
            )
        ]

        assert guild.basic.mark is None
        assert (
            guild.basic.custom_mark
            == "iVBORw0KGgoAAAANSUhEUgAAABEAAAARCAYAAAA7bUf6AAAAf0lEQVQ4y92Q0Q2AIAxEr40zuIKjORNuhiPgEDUaJYgFbGL88H7oQbhcH/4lKmwjyUyKv4i1ABGB86Hk0QrZP2QXmObFhH8LEeeDpPPpnzZRNQ49KvzQWVpmnjTSNx41EVH8z2nA8RDPBrzYjvGCWEmHZa3XmOTLWyq0wX0rACtmD0XA3MLsTAAAAABJRU5ErkJggg=="
        )

        mocker.stop(patcher)
