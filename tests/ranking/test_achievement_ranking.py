import pytest

import maplestory.utils.kst as kst
from maplestory.error import APIError
from maplestory.models.ranking.achievement import (
    AchievementRanking,
    AchievementRankingInfo,
)
from maplestory.services.rankings.achievement import (
    get_achievement_ranking,
    get_character_achievement_rank,
)


class TestGetAchievementRanking:
    # Tests retrieving achievement ranking for a character with a valid name and specific date
    def test_retrieve_with_valid_name_and_specific_date(self):
        character_name = "온앤온"
        date = kst.datetime(2024, 2, 27)

        result = get_achievement_ranking(character_name=character_name, date=date)
        rank = result[0]

        assert isinstance(result, AchievementRanking)
        assert isinstance(rank, AchievementRankingInfo)
        assert rank.date == date
        assert rank.character_name == character_name
        assert rank.ranking == 66135
        assert rank.world_name == "스카니아"
        assert rank.class_name == "마법사"
        assert rank.sub_class_name == "아크메이지(썬,콜)"
        assert rank.trophy_grade == "실버"
        assert rank.trophy_score == 13620

    # Tests error handling when an invalid character name is provided
    def test_error_handling_invalid_character_name(self):
        character_name = "NotExistentCharacter"

        with pytest.raises(APIError, match="Please input valid parameter"):
            get_achievement_ranking(character_name=character_name)

    # Tests retrieving achievement ranking for a character with valid name and yesterday's date
    def test_retrieve_with_valid_name_and_yesterday(self):
        character_name = "온앤온"
        date = kst.yesterday()

        result = get_achievement_ranking(character_name=character_name, date=date)
        rank = result[0]

        assert isinstance(result, AchievementRanking)
        assert isinstance(rank, AchievementRankingInfo)
        assert rank.date == date
        assert rank.character_name == character_name

    # Tests error handling when a future date is provided
    def test_error_handling_future_date(self):
        character_name = "온앤온"
        date = kst.datetime(2099, 1, 1)

        with pytest.raises(APIError, match="Please wait until the data is ready"):
            get_achievement_ranking(character_name=character_name, date=date)

    # Tests retrieving achievement ranking for a character with valid name and page number equal to 1
    def test_retrieve_with_valid_name_and_page_one(self):
        character_name = "온앤온"
        page_number = 1

        result = get_achievement_ranking(
            character_name=character_name, page_number=page_number
        )
        rank = result[0]

        assert isinstance(result, AchievementRanking)
        assert isinstance(rank, AchievementRankingInfo)
        assert rank.date == kst.yesterday()
        assert rank.character_name == character_name

    # Tests retrieving achievement ranking for a character with valid name and page number greater than 1
    def test_retrieve_with_valid_name_and_higher_page_number(self):
        character_name = "온앤온"
        page_number = 2
        date = kst.yesterday()

        result = get_achievement_ranking(
            character_name=character_name, page_number=page_number, date=date
        )
        rank = result[0]

        assert isinstance(result, AchievementRanking)
        assert isinstance(rank, AchievementRankingInfo)
        assert rank.date == date
        assert rank.character_name == character_name

    # Tests error handling when a page number less than 1 is provided
    def test_error_handling_page_number_less_than_one(self):
        character_name = "온앤온"
        page_number = 0
        date = kst.yesterday()

        with pytest.raises(APIError, match="Please input valid parameter"):
            get_achievement_ranking(
                character_name=character_name, page_number=page_number, date=date
            )

    # Tests error handling for a date in the far past
    def test_error_handling_far_past_date(self):
        date = kst.datetime(2000, 1, 1)

        with pytest.raises(
            ValueError,
            match="RANKING{은,는} 2023-12-22부터 데이터를 조회할 수 있습니다.",
        ):
            get_achievement_ranking(date=date)


class TestGetCharacterAchievementRank:
    # Tests retrieving achievement ranking info for a character with a valid name and date
    def test_retrieve_with_valid_name_and_date(self):
        character_name = "온앤온"
        date = kst.datetime(2024, 2, 27)

        rank = get_character_achievement_rank(character_name=character_name, date=date)

        assert isinstance(rank, AchievementRankingInfo)
        assert rank.date == date
        assert rank.character_name == character_name
        assert rank.ranking == 66135
        assert rank.world_name == "스카니아"
        assert rank.class_name == "마법사"
        assert rank.sub_class_name == "아크메이지(썬,콜)"
        assert rank.trophy_grade == "실버"
        assert rank.trophy_score == 13620

    # Tests handling None as character name
    def test_handle_none_character_name(self):
        character_name = None

        result = get_character_achievement_rank(character_name=character_name)

        assert result is None

    # Tests handling an empty character name
    def test_handle_empty_character_name(self):
        character_name = ""

        result = get_character_achievement_rank(character_name=character_name)

        assert result is None

    # Tests error handling for a future date
    def test_handle_future_date(self):
        character_name = "온앤온"
        date = kst.datetime(2099, 1, 1)

        with pytest.raises(APIError, match="Please wait until the data is ready"):
            get_character_achievement_rank(character_name=character_name, date=date)

    # Tests error handling for a date before the data availability
    def test_handle_past_date_error(self):
        character_name = "온앤온"
        date = kst.datetime(2023, 12, 21)

        with pytest.raises(
            ValueError,
            match="RANKING{은,는} 2023-12-22부터 데이터를 조회할 수 있습니다.",
        ):
            get_character_achievement_rank(character_name=character_name, date=date)
