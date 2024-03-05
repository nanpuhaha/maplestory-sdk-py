import pytest
from pydantic import ValidationError

import maplestory.utils.kst as kst
from maplestory.enums import GuildRankTypeEnum
from maplestory.models.ranking.guild import (
    AllGuildRankingInfo,
    GuildRankingTypePoint,
    GuildTypeRanking,
    GuildTypeRankingInfo,
)
from maplestory.services.rankings.guild import (
    get_all_type_guild_ranking,
    get_flag_race_guild_ranking,
    get_guild_ranking,
    get_sewer_guild_ranking,
    get_weekly_fame_guild_ranking,
    get_world_guild_ranking,
    group_by_guild,
)
from maplestory.utils.kst import datetime, is_same_date


class TestGetWorldGuildRanking:
    # Tests retrieving guild ranking for a specific world using default parameters
    def test_default_parameters(self):
        world_name = "스카니아"
        result = get_world_guild_ranking(world_name=world_name)
        assert isinstance(result, GuildTypeRanking)
        assert len(result.ranking) > 0

    # Tests retrieving guild ranking for a non-existent world
    def test_nonexistent_world(self):
        world_name = "nonexistent_world"
        result = get_world_guild_ranking(world_name=world_name)
        assert isinstance(result, GuildTypeRanking)
        assert len(result.ranking) == 0

    # Tests retrieving guild ranking with custom ranking type and page number
    def test_custom_parameters(self):
        world_name = "스카니아"
        ranking_type = 1  # Assuming 1 represents a specific type of ranking
        page_number = 2
        date = kst.datetime(2023, 12, 22)

        result = get_world_guild_ranking(
            world_name=world_name,
            ranking_type=ranking_type,
            page_number=page_number,
            date=date,
        )
        assert isinstance(result, GuildTypeRanking)
        assert len(result.ranking) > 0

    # Tests retrieving guild ranking with a custom date
    def test_custom_date(self):
        world_name = "스카니아"
        ranking_type = 1  # Assuming again that 1 represents a specific ranking type
        page_number = 2
        date = kst.datetime(2023, 12, 31)

        result = get_world_guild_ranking(
            world_name=world_name,
            ranking_type=ranking_type,
            page_number=page_number,
            date=date,
        )
        assert isinstance(result, GuildTypeRanking)
        assert len(result.ranking) > 0


class TestGetGuildRanking:
    # Tests retrieving guild ranking for a specific guild with default parameters
    def test_default_parameters_guild_ranking(self):
        guild_name = "온앤온"
        ranking = get_guild_ranking(guild=guild_name)
        assert isinstance(ranking, GuildTypeRanking)
        if len(ranking) == 0:
            pytest.skip("No results for the specified guild")
        rank = ranking[0]  # Assuming the function returns a list
        assert rank.guild_name == guild_name
        assert rank.world_name == "스카니아"
        assert rank.guild_master_name == "온앤온"
        assert rank.type == GuildRankTypeEnum.WEEKLY_FAME

    # Tests retrieving guild ranking with custom parameters including world name and ranking type
    def test_custom_parameters_guild_ranking(self):
        ranking = get_guild_ranking(
            guild="리더",
            ranking_type=GuildRankTypeEnum.FLAG_RACE,
            world_name="스카니아",
            page_number=2,
            date=kst.datetime(2023, 12, 22),
        )
        assert isinstance(ranking, GuildTypeRanking)
        rank = ranking[0]  # Assuming the function returns a list
        assert rank.guild_name == "리더"
        assert rank.world_name == "스카니아"
        assert rank.type == GuildRankTypeEnum.FLAG_RACE
        assert rank.date == kst.datetime(2023, 12, 22)

    # Corrects the test case name to reflect testing retrieval for a guild in an existent world
    def test_typo_in_method_name_and_error_handling(self):
        # Corrects expected error handling for a function call missing required arguments
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'guild'"
        ):
            get_guild_ranking(world_name="스카니아")

    # Tests error handling when retrieving ranking for a non-existent guild
    def test_nonexistent_guild_error_handling(self):
        ranking = get_guild_ranking(guild="NonExistentGuild")
        assert isinstance(ranking, GuildTypeRanking)
        assert len(ranking) == 0  # Expecting no results for a non-existent guild

    # Tests retrieving guild ranking for a guild on a specific date
    def test_specific_date_guild(self):
        ranking = get_guild_ranking(
            "리더",
            date=kst.datetime(2024, 2, 27),
        )
        assert isinstance(ranking, GuildTypeRanking)
        assert len(ranking) == 4

        first_rank = ranking[0]
        assert first_rank.ranking == 111
        assert first_rank.guild_name == "리더"
        assert first_rank.world_name == "스카니아"
        assert first_rank.guild_level == 30
        assert first_rank.guild_master_name == "아델"
        assert first_rank.guild_point == 313600
        assert first_rank.type == GuildRankTypeEnum.WEEKLY_FAME
        assert first_rank.date == kst.datetime(2024, 2, 27)
        assert first_rank.guild_mark == ""


class TestGroupByGuild:
    # Tests grouping a complex list of guild rankings across different worlds and rank types
    def test_group_by_multiple_guilds_across_worlds_and_rank_types(self):
        guild_rankings = [
            {
                "date": "2024-02-27",
                "world_name": "스카니아",
                "guild_name": "리더",
                "guild_level": 30,
                "guild_mark": "",
                "guild_point": 313600,
                "ranking": 111,
                "guild_master_name": "아델",
                "type": GuildRankTypeEnum.WEEKLY_FAME,
            },
            {
                "date": "2024-02-27",
                "world_name": "버닝",
                "guild_name": "리더",
                "guild_level": 27,
                "guild_mark": "",
                "guild_point": 127810,
                "ranking": 1497,
                "guild_master_name": "금은밍",
                "type": GuildRankTypeEnum.WEEKLY_FAME,
            },
            {
                "date": "2024-02-27",
                "world_name": "리부트2",
                "guild_name": "리더",
                "guild_level": 29,
                "guild_mark": "",
                "guild_point": 105350,
                "ranking": 1921,
                "guild_master_name": "승질난아델",
                "type": GuildRankTypeEnum.WEEKLY_FAME,
            },
            {
                "date": "2024-02-27",
                "world_name": "레드",
                "guild_name": "리더",
                "guild_level": 11,
                "guild_mark": "",
                "guild_point": 240,
                "ranking": 23543,
                "guild_master_name": "SATR",
                "type": GuildRankTypeEnum.WEEKLY_FAME,
            },
            {
                "date": "2024-02-27",
                "world_name": "스카니아",
                "guild_name": "리더",
                "guild_level": 30,
                "guild_mark": "",
                "guild_point": 6100,
                "ranking": 227,
                "guild_master_name": "아델",
                "type": GuildRankTypeEnum.FLAG_RACE,
            },
            {
                "date": "2024-02-27",
                "world_name": "버닝",
                "guild_name": "리더",
                "guild_level": 27,
                "guild_mark": "",
                "guild_point": 850,
                "ranking": 2432,
                "guild_master_name": "금은밍",
                "type": GuildRankTypeEnum.FLAG_RACE,
            },
            {
                "date": "2024-02-27",
                "world_name": "리부트2",
                "guild_name": "리더",
                "guild_level": 29,
                "guild_mark": "",
                "guild_point": 200,
                "ranking": 3018,
                "guild_master_name": "승질난아델",
                "type": GuildRankTypeEnum.FLAG_RACE,
            },
            {
                "date": "2024-02-27",
                "world_name": "스카니아",
                "guild_name": "리더",
                "guild_level": 30,
                "guild_mark": "",
                "guild_point": 1022559,
                "ranking": 7,
                "guild_master_name": "아델",
                "type": GuildRankTypeEnum.SEWER,
            },
            {
                "date": "2024-02-27",
                "world_name": "리부트2",
                "guild_name": "리더",
                "guild_level": 29,
                "guild_mark": "",
                "guild_point": 24466,
                "ranking": 1706,
                "guild_master_name": "승질난아델",
                "type": GuildRankTypeEnum.SEWER,
            },
            {
                "date": "2024-02-27",
                "world_name": "버닝",
                "guild_name": "리더",
                "guild_level": 27,
                "guild_mark": "",
                "guild_point": 4191,
                "ranking": 3300,
                "guild_master_name": "금은밍",
                "type": GuildRankTypeEnum.SEWER,
            },
        ]

        expected_result = {
            "리더 (스카니아)": [
                {
                    "date": "2024-02-27",
                    "world_name": "스카니아",
                    "guild_name": "리더",
                    "guild_level": 30,
                    "guild_mark": "",
                    "guild_point": 313600,
                    "ranking": 111,
                    "guild_master_name": "아델",
                    "type": GuildRankTypeEnum.WEEKLY_FAME,
                },
                {
                    "date": "2024-02-27",
                    "world_name": "스카니아",
                    "guild_name": "리더",
                    "guild_level": 30,
                    "guild_mark": "",
                    "guild_point": 6100,
                    "ranking": 227,
                    "guild_master_name": "아델",
                    "type": GuildRankTypeEnum.FLAG_RACE,
                },
                {
                    "date": "2024-02-27",
                    "world_name": "스카니아",
                    "guild_name": "리더",
                    "guild_level": 30,
                    "guild_mark": "",
                    "guild_point": 1022559,
                    "ranking": 7,
                    "guild_master_name": "아델",
                    "type": GuildRankTypeEnum.SEWER,
                },
            ],
            "리더 (버닝)": [
                {
                    "date": "2024-02-27",
                    "world_name": "버닝",
                    "guild_name": "리더",
                    "guild_level": 27,
                    "guild_mark": "",
                    "guild_point": 127810,
                    "ranking": 1497,
                    "guild_master_name": "금은밍",
                    "type": GuildRankTypeEnum.WEEKLY_FAME,
                },
                {
                    "date": "2024-02-27",
                    "world_name": "버닝",
                    "guild_name": "리더",
                    "guild_level": 27,
                    "guild_mark": "",
                    "guild_point": 850,
                    "ranking": 2432,
                    "guild_master_name": "금은밍",
                    "type": GuildRankTypeEnum.FLAG_RACE,
                },
                {
                    "date": "2024-02-27",
                    "world_name": "버닝",
                    "guild_name": "리더",
                    "guild_level": 27,
                    "guild_mark": "",
                    "guild_point": 4191,
                    "ranking": 3300,
                    "guild_master_name": "금은밍",
                    "type": GuildRankTypeEnum.SEWER,
                },
            ],
            "리더 (리부트2)": [
                {
                    "date": "2024-02-27",
                    "world_name": "리부트2",
                    "guild_name": "리더",
                    "guild_level": 29,
                    "guild_mark": "",
                    "guild_point": 105350,
                    "ranking": 1921,
                    "guild_master_name": "승질난아델",
                    "type": GuildRankTypeEnum.WEEKLY_FAME,
                },
                {
                    "date": "2024-02-27",
                    "world_name": "리부트2",
                    "guild_name": "리더",
                    "guild_level": 29,
                    "guild_mark": "",
                    "guild_point": 200,
                    "ranking": 3018,
                    "guild_master_name": "승질난아델",
                    "type": GuildRankTypeEnum.FLAG_RACE,
                },
                {
                    "date": "2024-02-27",
                    "world_name": "리부트2",
                    "guild_name": "리더",
                    "guild_level": 29,
                    "guild_mark": "",
                    "guild_point": 24466,
                    "ranking": 1706,
                    "guild_master_name": "승질난아델",
                    "type": GuildRankTypeEnum.SEWER,
                },
            ],
            "리더 (레드)": [
                {
                    "date": "2024-02-27",
                    "world_name": "레드",
                    "guild_name": "리더",
                    "guild_level": 11,
                    "guild_mark": "",
                    "guild_point": 240,
                    "ranking": 23543,
                    "guild_master_name": "SATR",
                    "type": GuildRankTypeEnum.WEEKLY_FAME,
                }
            ],
        }

        result = group_by_guild(guild_rankings)
        assert result == expected_result

    # Tests grouping rankings by guild and world names for a single guild with multiple rank types
    def test_group_by_guild_with_multiple_rank_types(self):
        guild_rankings = [
            {
                "date": "2024-02-25",
                "ranking": 25279,
                "guild_name": "온앤온",
                "world_name": "스카니아",
                "guild_level": 11,
                "guild_master_name": "온앤온",
                "guild_mark": "",
                "guild_point": 11600,
                "type": GuildRankTypeEnum.WEEKLY_FAME,
            },
            {
                "date": "2024-02-25",
                "ranking": 3721,
                "guild_name": "온앤온",
                "world_name": "스카니아",
                "guild_level": 11,
                "guild_master_name": "온앤온",
                "guild_mark": "",
                "guild_point": 15596,
                "type": GuildRankTypeEnum.SEWER,
            },
            {
                "date": "2024-02-25",
                "ranking": 12345,
                "guild_name": "온앤온",
                "world_name": "스카니아",
                "guild_level": 11,
                "guild_master_name": "온앤온",
                "guild_mark": "",
                "guild_point": 7890,
                "type": GuildRankTypeEnum.FLAG_RACE,
            },
        ]

        expected_result = {"온앤온 (스카니아)": guild_rankings}

        result = group_by_guild(guild_rankings)
        assert result == expected_result

    # Tests that an empty list of rankings returns an empty dictionary
    def test_group_by_empty_list_returns_empty_dict(self):
        guild_rankings = []
        result = group_by_guild(guild_rankings)
        assert result == {}


class TestGetAllTypeGuildRanking:
    # Tests retrieving comprehensive guild ranking information for a specific guild in a given world on a specified date
    def test_retrieve_comprehensive_guild_info_for_specific_guild(self):
        guild = "온앤온"
        world_name = "스카니아"
        date = kst.datetime(2024, 2, 25)

        result = get_all_type_guild_ranking(
            guild=guild, world_name=world_name, date=date
        )

        # Verifies that the result is an instance of AllGuildRankingInfo and checks various attributes
        assert isinstance(result, AllGuildRankingInfo)
        assert result.date == date
        assert result.world_name == world_name
        assert result.guild_name == guild
        assert (
            result.guild_level == 11
        )  # Assuming this is the correct guild level for the test case
        assert (
            result.guild_master_name == "온앤온"
        )  # Assuming the guild master's name for validation
        assert result.guild_mark == ""  # Assuming no guild mark for simplicity
        # Verifies the presence and accuracy of ranking points for specific guild ranking types
        assert isinstance(result.weekly_fame, GuildRankingTypePoint)
        assert result.weekly_fame.rank == 4288
        assert result.weekly_fame.point == 11600
        assert (
            result.flag_race is None
        )  # Assumes no flag race ranking is available or applicable
        assert isinstance(result.sewer, GuildRankingTypePoint)
        assert result.sewer.rank == 570
        assert result.sewer.point == 15596

    # Tests the behavior when attempting to retrieve guild rankings for a guild name that does not exist
    def test_handle_nonexistent_guild_name_error(self):
        guild = "NonexistentGuild"
        world_name = "스카니아"
        date = kst.datetime(2024, 2, 25)

        # Expects a ValidationError to be raised due to the nonexistence of the specified guild
        with pytest.raises(ValidationError):
            get_all_type_guild_ranking(guild=guild, world_name=world_name, date=date)


class TestGetWeeklyFameGuildRanking:
    # Retrieve weekly fame guild ranking for a specific date, world, and page number
    def test_retrieve_weekly_fame_guild_ranking_for_specific_world_and_guild(self):
        ranking = get_weekly_fame_guild_ranking(
            world_name="스카니아", guild="온앤온", page_number=1, date=kst.yesterday()
        )
        if len(ranking) == 0:
            pytest.skip("No results for the specified guild in the specified world")

        rank = ranking[0]

        assert isinstance(ranking, GuildTypeRanking)
        assert isinstance(rank, GuildTypeRankingInfo)
        assert rank.type == GuildRankTypeEnum.WEEKLY_FAME
        assert rank.world_name == "스카니아"
        assert rank.guild_name == "온앤온"
        assert is_same_date(rank.date, kst.yesterday())

    # Retrieve weekly fame guild ranking for a date before 2023-12-22
    def test_retrieve_weekly_fame_guild_ranking_for_date_before_2023_12_22(self):
        with pytest.raises(
            ValueError,
            match="RANKING{은,는} 2023-12-22부터 데이터를 조회할 수 있습니다.",
        ):
            get_weekly_fame_guild_ranking(date=datetime(2022, 12, 21))


class TestGetFlagRaceGuildRanking:
    # Tests retrieving Flag Race guild ranking with default parameters
    def test_default_parameters_flag_race_ranking(self):
        result = get_flag_race_guild_ranking()
        assert isinstance(result, GuildTypeRanking)

    # Tests handling of an invalid world name for Flag Race guild ranking retrieval
    def test_invalid_world_name_handling(self):
        result = get_flag_race_guild_ranking(world_name="InvalidWorldName")
        assert len(result) == 0  # Expecting no results for an invalid world name

    # Tests retrieving Flag Race guild ranking with valid parameters (redundant, consider merging with the first test)
    def test_valid_parameters_flag_race_ranking(self):
        result = get_flag_race_guild_ranking()
        assert isinstance(result, GuildTypeRanking)

    # Tests retrieving Flag Race guild ranking for a specific, valid world name
    def test_specific_valid_world_name_flag_race_ranking(self):
        result = get_flag_race_guild_ranking(world_name="스카니아")
        assert isinstance(result, GuildTypeRanking)

    # Tests retrieving Flag Race guild ranking for a specific date (currently not passing any date to the function)
    def test_specific_date_flag_race_ranking(self):
        result = get_flag_race_guild_ranking(
            date=kst.yesterday()
        )  # Assuming functionality to pass a date is implemented
        assert isinstance(result, GuildTypeRanking)

    # Tests retrieving Flag Race guild ranking for a specific guild in a valid world
    def test_specific_guild_flag_race_ranking(self):
        result = get_flag_race_guild_ranking(
            world_name="스카니아",
            guild="TestGuild",
            page_number=1,
            date=kst.yesterday(),
        )
        assert isinstance(result, GuildTypeRanking)

    # Tests retrieving Flag Race guild ranking for a specific page number
    def test_specific_page_number_flag_race_ranking(self):
        result = get_flag_race_guild_ranking(page_number=1)
        assert isinstance(result, GuildTypeRanking)


class TestGetSewerGuildRanking:
    # Tests retrieving Sewer guild ranking for a specific guild in a given world on a specified date
    def test_retrieve_specific_sewer_guild_ranking(self):
        # Call the function under test with specific parameters
        result = get_sewer_guild_ranking(
            world_name="스카니아",
            guild="리더",
            page_number=1,
            date=kst.datetime(2024, 2, 27),
        )
        rank = result[0]  # Assuming the function returns a list of GuildTypeRankingInfo

        # Validate the result's structure and content
        assert isinstance(
            result, GuildTypeRanking
        )  # Ensure the result is a GuildTypeRanking object
        assert len(result.ranking) > 0  # Ensure the ranking list is not empty
        assert isinstance(
            rank, GuildTypeRankingInfo
        )  # Ensure individual rankings are of correct type
        # Verify the correctness of the ranking information
        assert rank.type == GuildRankTypeEnum.SEWER  # Check the ranking type is Sewer
        assert rank.world_name == "스카니아"  # Check the world name matches
        assert rank.guild_name == "리더"  # Check the guild name matches
        assert rank.date == kst.datetime(2024, 2, 27)  # Ensure the date matches
        assert rank.ranking == 2  # Verify the ranking position
        assert rank.guild_level == 30  # Verify the guild level
        assert rank.guild_master_name == "아델"  # Check the guild master's name
        assert rank.guild_point == 1022559  # Check the guild points
