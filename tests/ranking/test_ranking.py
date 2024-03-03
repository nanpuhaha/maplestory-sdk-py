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
from maplestory.enums import QueryableDateEnum, WorldTypeEnum
from maplestory.error import APIError
from maplestory.models.ranking.achievement import AchievementRanking
from maplestory.models.ranking.dojang import DojangRanking
from maplestory.models.ranking.guild import GuildTypeRanking
from maplestory.models.ranking.overall import OverallRanking
from maplestory.models.ranking.theseed import TheSeedRanking
from maplestory.models.ranking.union import UnionRanking
from maplestory.services.character import get_character_id


class TestGetOverallRanking:
    # Tests retrieving overall ranking using default parameters
    def test_default_parameters(self):
        result = get_overall_ranking_by_id()
        assert isinstance(result, OverallRanking)

    # Tests retrieving overall ranking for a specific world
    def test_specific_world(self):
        result = get_overall_ranking_by_id(world_name="스카니아")
        assert isinstance(result, OverallRanking)
        assert all(rank.world_name == "스카니아" for rank in result)

    # Tests filtering overall ranking by normal world type
    def test_filter_by_normal_world_type(self):
        result = get_overall_ranking_by_id(world_type=WorldTypeEnum.일반)
        assert isinstance(result, OverallRanking)
        assert not any("리부트" in rank.world_name for rank in result)

    # Tests filtering overall ranking by reboot world type
    def test_filter_by_reboot_world_type(self):
        result = get_overall_ranking_by_id(world_type=WorldTypeEnum.리부트)
        assert isinstance(result, OverallRanking)
        assert all("리부트" in rank.world_name for rank in result)

    # Tests retrieving overall ranking for the earliest date available
    def test_earliest_date(self):
        result = get_overall_ranking_by_id(date=QueryableDateEnum.랭킹.value)
        assert isinstance(result, OverallRanking)

    # Tests retrieving overall ranking for the most recent date
    def test_latest_date(self):
        result = get_overall_ranking_by_id(date=kst.yesterday())
        assert isinstance(result, OverallRanking)

    # Tests filtering overall ranking by job class
    def test_filter_by_job_class(self):
        job_class = "초보자-전체 전직"
        result = get_overall_ranking_by_id(job_class=job_class)
        assert isinstance(result, OverallRanking)
        assert all(rank.class_name == "초보자" for rank in result)

    # Tests retrieving overall ranking for a specific character
    def test_specific_character(self):
        character_name = "온앤온"
        character_id = get_character_id(character_name)
        result = get_overall_ranking_by_id(character_id=character_id)
        assert isinstance(result, OverallRanking)
        assert len(result) == 1
        assert result[0].character_name == character_name


class TestGetUnionRanking:
    # Tests retrieving union ranking for a specific world
    def test_for_world(self):
        result = get_union_ranking_by_id(
            world_name="스카니아", date=kst.datetime(2023, 12, 22)
        )
        assert isinstance(result, UnionRanking)

    # Tests retrieving union ranking for a specific character
    def test_for_character(self):
        character_id = get_character_id("온앤온")
        result = get_union_ranking_by_id(
            character_id=character_id, date=kst.datetime(2023, 12, 22)
        )
        assert isinstance(result, UnionRanking)

    # Tests retrieving union ranking for a specific page number
    def test_for_page_number(self):
        result = get_union_ranking_by_id(page_number=2, date=kst.datetime(2023, 12, 22))
        assert isinstance(result, UnionRanking)

    # Tests error handling for dates without timezone information
    def test_date_without_timezone(self):
        with pytest.raises(ValueError, match="datetime should have timezone info."):
            get_union_ranking_by_id(date=datetime.now())

    # Tests error handling for dates not in KST timezone
    def test_date_not_in_kst_timezone(self):
        with pytest.raises(ValueError, match="datetime should have KST timezone info."):
            get_union_ranking_by_id(date=datetime(2023, 12, 22, tzinfo=timezone.utc))

    # Tests error handling for dates earlier than the queryable date range
    def test_date_earlier_than_queryable(self):
        with pytest.raises(ValueError):
            get_union_ranking_by_id(date=kst.datetime(2023, 12, 21))


class TestGetGuildRanking:
    # Tests retrieving guild ranking based on world name
    def test_by_world_name(self):
        result = get_guild_ranking_by_id(
            ranking_type=0, world_name="스카니아", date=kst.yesterday()
        )
        assert isinstance(result, GuildTypeRanking)

    # Tests retrieving guild ranking based on guild name
    def test_by_guild_name(self):
        result = get_guild_ranking_by_id(
            ranking_type=0, guild="리더", date=kst.yesterday()
        )
        assert isinstance(result, GuildTypeRanking)

    # Tests retrieving guild ranking for a non-existing guild name
    def test_nonexistent_guild_name(self):
        result = get_guild_ranking_by_id(
            ranking_type=0, guild="Not Exist Guild Name", date=kst.yesterday()
        )
        assert len(result) == 0

    # Tests retrieving guild ranking based on page number
    def test_by_page_number(self):
        result = get_guild_ranking_by_id(
            ranking_type=0, page_number=2, date=kst.yesterday()
        )
        assert isinstance(result, GuildTypeRanking)

    # Tests error handling for invalid ranking type
    def test_invalid_ranking_type_error(self):
        with pytest.raises(ValueError):
            get_guild_ranking_by_id(ranking_type=3, date=kst.yesterday())

    # Tests error handling for querying a date earlier than allowed
    def test_earlier_date_error(self):
        with pytest.raises(ValueError):
            get_guild_ranking_by_id(date=kst.datetime(2023, 12, 20))

    # Tests retrieving today's ranking, considering the update time
    def test_today_ranking_condition(self):
        if kst.now() < kst.today_with_time(hour=8, minute=30):
            with pytest.raises(ValueError):
                get_guild_ranking_by_id(date=kst.today())
        else:
            result = get_guild_ranking_by_id(date=kst.today())
            assert isinstance(result, GuildTypeRanking)


class TestGetDojangRanking:
    # Tests retrieving dojang ranking with default parameters
    def test_default_retrieval(self):
        character_id = get_character_id("온앤온")
        ranking = get_dojang_ranking_by_id(character_id=character_id)
        assert isinstance(ranking, DojangRanking)

    # Tests retrieving dojang ranking for a future date
    def test_future_date_retrieval(self):
        character_id = get_character_id("온앤온")
        ranking = get_dojang_ranking_by_id(
            character_id=character_id, date=kst.datetime(2024, 1, 1)
        )
        assert isinstance(ranking, DojangRanking)

    # Tests error handling for invalid difficulty level
    def test_invalid_difficulty_error(self):
        with pytest.raises(ValueError):
            get_dojang_ranking_by_id(difficulty_level=2)

    # Tests error handling for querying a date earlier than allowed
    def test_minimum_date_error(self):
        with pytest.raises(ValueError):
            get_dojang_ranking_by_id(date=kst.datetime(2023, 12, 21))

    # Tests error handling for a future date query
    def test_future_date_error(self):
        with pytest.raises(APIError, match="Please wait until the data is ready"):
            get_dojang_ranking_by_id(date=kst.datetime(2099, 12, 31))


class TestGetTheseedRanking:
    # Tests retrieving TheSeedRanking with valid world name, page number, and date
    def test_with_valid_arguments(self):
        result = get_theseed_ranking_by_id(
            world_name="스카니아", page_number=1, date=kst.yesterday()
        )
        assert isinstance(result, TheSeedRanking)

    # Tests retrieving TheSeedRanking with only the date specified
    def test_with_only_date(self):
        result = get_theseed_ranking_by_id(date=kst.yesterday())
        assert isinstance(result, TheSeedRanking)

    # Tests retrieving TheSeedRanking with only the page number specified
    def test_with_only_page_number(self):
        result = get_theseed_ranking_by_id(page_number=2)
        assert isinstance(result, TheSeedRanking)

    # Tests error handling for a non-timezone aware datetime
    def test_date_not_timezone_aware(self):
        with pytest.raises(ValueError):
            get_theseed_ranking_by_id(date=datetime.now())

    # Tests error handling for a date outside the queryable range
    def test_date_outside_queryable_range(self):
        with pytest.raises(ValueError):
            get_theseed_ranking_by_id(date=datetime(2023, 12, 20))

    # Tests handling API errors
    def test_api_error_handling(self):
        with pytest.raises(APIError):
            get_theseed_ranking_by_id(character_id="0000")


class TestGetAchievementRanking:
    # Tests retrieving AchievementRanking for a specific date
    def test_for_specific_date(self):
        result = get_achievement_ranking_by_id(date=kst.datetime(2023, 12, 22))
        assert isinstance(result, AchievementRanking)

    # Tests error handling for non-timezone aware datetime
    def test_datetime_not_timezone_aware(self):
        with pytest.raises(ValueError, match="datetime should have timezone info"):
            get_achievement_ranking_by_id(date=datetime(2023, 12, 22))

    # Tests retrieving AchievementRanking for a given page number and date
    def test_for_page_number_and_date(self):
        result = get_achievement_ranking_by_id(
            page_number=2, date=kst.datetime(2023, 12, 22)
        )
        assert isinstance(result, AchievementRanking)
