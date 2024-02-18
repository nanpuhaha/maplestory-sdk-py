from datetime import datetime, timezone

import pytest

import maplestory.utils.kst as kst
from maplestory.apis.ranking import (
    get_achievement_ranking_by_id,
    get_dojang_ranking_by_id,
    get_guild_ranking_by_id,
    get_overall_ranking_by_id,
    get_theseed_ranking_by_id,
    get_union_ranking_by_id,
)
from maplestory.enums import QueryableDate, WorldType
from maplestory.error import APIError
from maplestory.models.ranking.achievement import AchievementRanking
from maplestory.models.ranking.dojang import DojangRanking
from maplestory.models.ranking.guild import GuildRanking
from maplestory.models.ranking.overall import OverallRanking
from maplestory.models.ranking.theseed import TheSeedRanking
from maplestory.models.ranking.union import UnionRanking
from maplestory.services.character import get_character_id
from maplestory.utils.params import every_element_contains, every_element_not_contains


class TestGetOverallRanking:
    # Retrieve overall ranking for a given date with default parameters
    def test_retrieve_overall_ranking_with_default_parameters(self):
        result = get_overall_ranking_by_id()
        assert isinstance(result, OverallRanking)

    # Retrieve overall ranking for a given date and world name
    def test_retrieve_overall_ranking_with_world_name(self):
        result = get_overall_ranking_by_id(world_name="스카니아")
        assert isinstance(result, OverallRanking)
        assert {rank.world_name for rank in result} == {"스카니아"}

    # Retrieve overall ranking for a given date and world type
    def test_retrieve_overall_ranking_with_world_type(self):
        result = get_overall_ranking_by_id(world_type=WorldType.일반)
        assert isinstance(result, OverallRanking)

        world_names = {rank.world_name for rank in result}
        assert every_element_not_contains(world_names, "리부트")

    # Retrieve overall ranking for a given date and world type
    def test_retrieve_overall_ranking_with_world_type2(self):
        result = get_overall_ranking_by_id(world_type=WorldType.리부트)
        assert isinstance(result, OverallRanking)

        world_names = {rank.world_name for rank in result}
        assert every_element_contains(world_names, "리부트")

    # Retrieve overall ranking for the earliest possible date
    def test_retrieve_overall_ranking_for_earliest_date(self):
        result = get_overall_ranking_by_id(date=kst.datetime(2023, 12, 22))
        assert isinstance(result, OverallRanking)

        result = get_overall_ranking_by_id(date=QueryableDate.랭킹.value)
        assert isinstance(result, OverallRanking)

    # Retrieve overall ranking for the latest possible date
    def test_retrieve_overall_ranking_for_latest_date(self):
        result = get_overall_ranking_by_id(date=kst.yesterday())
        assert isinstance(result, OverallRanking)

    def test_retrieve_overall_ranking_with_job_class(self):
        job_class = "초보자-전체 전직"
        result = get_overall_ranking_by_id(job_class=job_class)
        assert isinstance(result, OverallRanking)

        class_names = {rank.class_name for rank in result}
        assert class_names == {"초보자"}

        class_names = {rank.sub_class_name for rank in result}
        assert class_names == {""}

    def test_retrieve_overall_ranking_with_character_name(self):
        character_name = "온앤온"
        character_id = get_character_id(character_name)
        result = get_overall_ranking_by_id(character_id=character_id)
        assert isinstance(result, OverallRanking)
        assert len(result) == 1
        assert result[0].character_name == character_name


class TestGetUnionRanking:
    # Retrieve union ranking for a specific world and date
    def test_retrieve_union_ranking_for_world_and_date(self):
        result = get_union_ranking_by_id(
            world="스카니아", date=kst.datetime(2023, 12, 22)
        )

        assert isinstance(result, UnionRanking)

    # Retrieve union ranking for a specific character and date
    def test_retrieve_union_ranking_for_character_and_date(self):
        character_id = get_character_id("온앤온")
        result = get_union_ranking_by_id(
            character_id=character_id, date=kst.datetime(2023, 12, 22)
        )

        assert isinstance(result, UnionRanking)

    # Retrieve union ranking for a specific page number and date
    def test_retrieve_union_ranking_for_page_number_and_date(self):
        result = get_union_ranking_by_id(page_number=2, date=kst.datetime(2023, 12, 22))

        assert isinstance(result, UnionRanking)

    # Raise ValueError if date argument is not timezone aware
    def test_raise_value_error_if_date_not_timezone_aware(self):
        with pytest.raises(ValueError):
            get_union_ranking_by_id(date=datetime.now())

    # Raise ValueError if date argument timezone is not KST
    def test_raise_value_error_if_date_timezone_not_kst(self):
        with pytest.raises(ValueError, match="datetime should have KST timezone info."):
            get_union_ranking_by_id(date=datetime(2023, 12, 22, tzinfo=timezone.utc))

    # Raise ValueError if date argument is earlier than QueryableDate.랭킹
    def test_raise_value_error_if_date_earlier_than_queryable_date(self):
        with pytest.raises(ValueError):
            get_union_ranking_by_id(date=kst.datetime(2023, 12, 21))


class TestGetGuildRanking:
    # Retrieve guild ranking for a given date, ranking type, and world name
    def test_retrieve_guild_ranking_with_world_name(self):
        result = get_guild_ranking_by_id(
            ranking_type=0, world_name="스카니아", date=kst.yesterday()
        )

        assert isinstance(result, GuildRanking)

    # Retrieve guild ranking for a given date, ranking type, and guild name
    def test_retrieve_guild_ranking_with_guild_name(self):
        result = get_guild_ranking_by_id(
            ranking_type=0, guild="리더", date=kst.yesterday()
        )

        assert isinstance(result, GuildRanking)

    # Retrieve guild ranking for a given date, ranking type, and guild name
    def test_retrieve_guild_ranking_with_not_existing_guild_name(self):
        result = get_guild_ranking_by_id(
            ranking_type=0, guild="Not Exist Guild Name", date=kst.yesterday()
        )

        # TODO: API returns empty list, but it should raise an error
        assert isinstance(result, GuildRanking)
        assert len(result) == 0
        assert result == GuildRanking(ranking=[])

    # Retrieve guild ranking for a given date, ranking type, and page number
    def test_retrieve_guild_ranking_with_page_number(self):
        result = get_guild_ranking_by_id(
            ranking_type=0, page_number=2, date=kst.yesterday()
        )

        assert isinstance(result, GuildRanking)

    # Raise ValueError if ranking_type is not 0, 1, or 2
    def test_raise_value_error_invalid_ranking_type(self):
        with pytest.raises(ValueError):
            get_guild_ranking_by_id(ranking_type=3, date=kst.yesterday())

    # Raise ValueError if date is earlier than QueryableDate.랭킹
    def test_raise_value_error_earlier_date(self):
        with pytest.raises(ValueError):
            get_guild_ranking_by_id(date=kst.datetime(2023, 12, 20))

    def test_today_ranking(self):
        if kst.now() < kst.today_with_time(hour=8, minute=30):
            with pytest.raises(ValueError):
                get_guild_ranking_by_id(date=kst.today())
        else:
            result = get_guild_ranking_by_id(date=kst.today())
            assert isinstance(result, GuildRanking)


class TestGetDojangRanking:
    # Retrieve dojang ranking for a valid character ID, with default parameters
    def test_retrieve_default_parameters(self):
        character_id = get_character_id("온앤온")
        ranking = get_dojang_ranking_by_id(character_id=character_id)

        assert isinstance(ranking, DojangRanking)

    # Retrieve dojang ranking for a valid character ID, with a date in the future
    def test_retrieve_future_date(self):
        character_id = get_character_id("온앤온")
        ranking = get_dojang_ranking_by_id(
            character_id=character_id, date=kst.datetime(2024, 1, 1)
        )

        assert isinstance(ranking, DojangRanking)

    # Raise a ValueError for an invalid difficulty level (not 0 or 1)
    def test_invalid_difficulty_level(self):
        with pytest.raises(ValueError):
            get_dojang_ranking_by_id(difficulty_level=2)

    # Raise a ValueError for a date earlier than the minimum queryable date
    def test_earlier_than_minimum_date(self):
        with pytest.raises(ValueError):
            get_dojang_ranking_by_id(date=kst.datetime(2023, 12, 21))

    # Raise a ValueError for a date in the future
    def test_future_date(self):
        with pytest.raises(APIError, match="Please wait until the data is ready"):
            get_dojang_ranking_by_id(date=kst.datetime(2099, 12, 31))


class TestGetTheseedRanking:
    # Should return TheSeedRanking object when valid arguments are passed
    def test_valid_arguments_passed(self):
        result = get_theseed_ranking_by_id(
            world_name="스카니아", page_number=1, date=kst.yesterday()
        )

        assert isinstance(result, TheSeedRanking)

    # Should return TheSeedRanking object when only date argument is passed
    def test_only_date_argument_passed(self):
        result = get_theseed_ranking_by_id(date=kst.yesterday())

        assert isinstance(result, TheSeedRanking)

    # Should return TheSeedRanking object when only page_number argument is passed
    def test_only_page_number_argument_passed(self):
        result = get_theseed_ranking_by_id(page_number=2)

        assert isinstance(result, TheSeedRanking)

    # Should raise ValueError when date argument is not AwareDatetime
    def test_date_argument_not_aware_datetime(self):
        with pytest.raises(ValueError):
            get_theseed_ranking_by_id(date=datetime.now())

    # Should raise ValueError when date argument is not within QueryableDate.랭킹
    def test_date_argument_not_within_queryable_date(self):
        with pytest.raises(ValueError):
            get_theseed_ranking_by_id(date=datetime(2023, 12, 20))

    # Should raise APIError when API returns error
    def test_api_returns_error(self):
        with pytest.raises(APIError):
            get_theseed_ranking_by_id(
                character_id="0000",
            )


class TestGetAchievementRanking:
    # Returns the achievement ranking for a given date and character ID.
    def test_returns_achievement_ranking_for_given_date_and_character_id(self):
        result = get_achievement_ranking_by_id(date=kst.datetime(2023, 12, 22))

        assert isinstance(result, AchievementRanking)

    def test_invalid_datetime(self):
        with pytest.raises(ValueError, match="datetime should have timezone info"):
            get_achievement_ranking_by_id(date=datetime(2023, 12, 22))

    # Returns the achievement ranking for a given date and page number.
    def test_returns_achievement_ranking_for_given_date_and_page_number(self):
        result = get_achievement_ranking_by_id(
            page_number=2, date=kst.datetime(2023, 12, 22)
        )

        assert isinstance(result, AchievementRanking)
