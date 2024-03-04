from datetime import datetime

import pytest

import maplestory.utils.kst as kst
from maplestory.error import APIError
from maplestory.models.ranking.theseed import TheSeedRanking, TheSeedRankingInfo
from maplestory.services.rankings.theseed import (
    get_character_theseed_rank,
    get_theseed_ranking,
    get_world_theseed_ranking,
)


class TestGetTheseedRanking:
    # Tests retrieval of TheSeedRanking without any specified parameters
    def test_retrieve_default(self):
        ranking = get_theseed_ranking()
        rank = ranking[0]
        assert isinstance(ranking, TheSeedRanking)
        assert isinstance(rank, TheSeedRankingInfo)
        assert rank.ranking == 1
        assert rank.date == kst.yesterday()

    # Tests retrieval of TheSeedRanking for a specific character
    def test_retrieve_for_specific_character(self):
        character_name = "캐논라보"
        ranking = get_theseed_ranking(character_name=character_name)
        rank = ranking[0]
        assert isinstance(ranking, TheSeedRanking)
        assert isinstance(rank, TheSeedRankingInfo)
        assert rank.date == kst.yesterday()
        assert rank.character_name == character_name

    # Tests handling of an invalid world name during TheSeedRanking retrieval
    def test_handle_invalid_world_name(self):
        world_name = "InvalidWorld"
        ranking = get_theseed_ranking(world_name=world_name)
        assert isinstance(ranking, TheSeedRanking)
        assert len(ranking) == 0

    # Tests handling of an invalid character name during TheSeedRanking retrieval
    def test_handle_invalid_character_name(self):
        character_name = "NonExistentCharacter"
        with pytest.raises(APIError, match="Please input valid parameter"):
            get_theseed_ranking(character_name=character_name)

    # Tests retrieval of TheSeedRanking with all provided valid arguments
    def test_retrieve_with_all_valid_arguments(self):
        world_name = "스카니아"
        character_name = "온앤온"
        page_number = 1
        date = kst.yesterday()
        ranking = get_theseed_ranking(
            world_name=world_name,
            character_name=character_name,
            page_number=page_number,
            date=date,
        )
        assert isinstance(ranking, TheSeedRanking)


class TestGetWorldTheseedRanking:
    # Tests retrieval of TheSeedRanking for a specific world with given page number and date
    def test_retrieve_for_specific_world(self):
        world_name = "스카니아"
        page_number = 2
        date = kst.yesterday()
        result = get_world_theseed_ranking(
            world_name=world_name, page_number=page_number, date=date
        )
        assert isinstance(result, TheSeedRanking)

    # Tests retrieval of TheSeedRanking with an invalid world name
    def test_retrieve_with_invalid_world_name(self):
        world_name = "InvalidWorld"
        result = get_world_theseed_ranking(world_name=world_name)
        assert isinstance(result, TheSeedRanking)
        assert len(result) == 0


class TestGetCharacterTheseedRank:
    # Tests retrieving TheSeedRankingInfo for a character with valid name and date
    def test_retrieve_for_valid_character_and_date(self):
        character_name = "캐논라보"
        date = kst.datetime(2024, 2, 26)
        rank = get_character_theseed_rank(character_name=character_name, date=date)
        assert isinstance(rank, TheSeedRankingInfo)
        assert rank.date == date
        assert rank.character_name == character_name
        assert rank.ranking == 1
        assert rank.world_name == "엘리시움"

    # Tests handling of retrieval with an empty character name
    def test_retrieve_with_empty_character_name(self):
        character_name = ""
        date = kst.datetime(2023, 12, 22)
        result = get_character_theseed_rank(character_name=character_name, date=date)
        assert result is None

    # Tests error handling for non-existent character name
    def test_error_handling_nonexistent_character_name(self):
        character_name = "NonExistentCharacter"
        date = kst.datetime(2023, 12, 22)
        with pytest.raises(APIError, match="Please input valid parameter"):
            get_character_theseed_rank(character_name=character_name, date=date)

    # Tests error handling for an invalid date
    def test_error_handling_invalid_date(self):
        character_name = "캐논라보"
        date = kst.datetime(2022, 12, 22)
        with pytest.raises(
            ValueError,
            match="RANKING{은,는} 2023-12-22부터 데이터를 조회할 수 있습니다.",
        ):
            get_character_theseed_rank(character_name=character_name, date=date)

    # Tests error handling for a future date
    def test_error_handling_future_date(self):
        character_name = "캐논라보"
        date = kst.datetime(2099, 1, 1)
        with pytest.raises(APIError, match="Please wait until the data is ready"):
            get_character_theseed_rank(character_name=character_name, date=date)

    # Tests error handling for a date without KST timezone information
    def test_error_handling_date_without_kst_timezone(self):
        character_name = "캐논라보"
        date = datetime(2023, 12, 22)
        with pytest.raises(ValueError, match="datetime should have timezone info."):
            get_character_theseed_rank(character_name=character_name, date=date)
