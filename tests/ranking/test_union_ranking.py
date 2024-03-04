from datetime import datetime

import pytest

import maplestory.utils.kst as kst
from maplestory.error import APIError
from maplestory.models.ranking.union import UnionRanking, UnionRankingInfo
from maplestory.services.rankings.union import (
    get_character_union_rank,
    get_union_ranking,
    get_world_union_ranking,
)


class TestGetUnionRanking:
    # Tests retrieving UnionRanking without any arguments
    def test_retrieve_default(self):
        ranking = get_union_ranking()
        rank = ranking[0]

        assert isinstance(ranking, UnionRanking)
        assert isinstance(rank, UnionRankingInfo)
        assert rank.ranking == 1
        assert rank.date == kst.yesterday()

    # Tests retrieving UnionRanking with a valid character name
    def test_retrieve_with_valid_character_name(self):
        character_name = "밥먹어친구야"
        ranking = get_union_ranking(character_name=character_name)
        rank = ranking[0]

        assert isinstance(ranking, UnionRanking)
        assert isinstance(rank, UnionRankingInfo)
        assert rank.date == kst.yesterday()
        assert rank.character_name == character_name

    # Tests retrieving UnionRanking with an invalid world name
    def test_retrieve_with_invalid_world_name(self):
        world_name = "InvalidWorld"
        ranking = get_union_ranking(world_name=world_name)

        assert isinstance(ranking, UnionRanking)
        assert len(ranking) == 0

    # Tests handling of invalid character name
    def test_retrieve_with_invalid_character_name(self):
        character_name = "NonExistentCharacter"
        with pytest.raises(APIError, match="Please input valid parameter"):
            get_union_ranking(character_name=character_name)

    # Tests retrieving UnionRanking with valid arguments
    def test_retrieve_with_valid_arguments(self):
        world_name = "스카니아"
        character_name = "온앤온"
        page_number = 1
        date = kst.yesterday()

        ranking = get_union_ranking(
            world_name=world_name,
            character_name=character_name,
            page_number=page_number,
            date=date,
        )
        assert isinstance(ranking, UnionRanking)


class TestGetWorldUnionRanking:
    # Tests retrieving UnionRanking for a valid world name and date
    def test_retrieve_with_valid_world_name_and_date(self):
        world_name = "스카니아"
        page_number = 2
        date = kst.yesterday()

        result = get_world_union_ranking(
            world_name=world_name, page_number=page_number, date=date
        )
        assert isinstance(result, UnionRanking)

    # Tests handling of invalid world name
    def test_retrieve_with_invalid_world_name(self):
        world_name = "InvalidWorld"
        result = get_world_union_ranking(world_name=world_name)
        assert isinstance(result, UnionRanking)
        assert len(result) == 0


class TestGetCharacterUnionRank:
    # Tests retrieving UnionRankingInfo for a valid character name and date
    def test_retrieve_with_valid_character_name_and_date(self):
        character_name = "밥먹어친구야"
        date = kst.datetime(2024, 2, 26)

        rank = get_character_union_rank(character_name=character_name, date=date)
        assert isinstance(rank, UnionRankingInfo)
        assert rank.date == date
        assert rank.character_name == character_name
        assert rank.ranking == 1
        assert rank.world_name == "베라"

    # Tests handling of empty character name
    def test_retrieve_with_empty_character_name(self):
        character_name = ""
        result = get_character_union_rank(character_name=character_name)
        assert result is None

    # Tests error handling for non-existent character name
    def test_retrieve_with_nonexistent_character_name(self):
        character_name = "NonExistentCharacter"
        with pytest.raises(APIError, match="Please input valid parameter"):
            get_character_union_rank(character_name=character_name)

    # Tests handling of invalid date
    def test_retrieve_with_invalid_date(self):
        character_name = "밥먹어친구야"
        date = kst.datetime(2022, 12, 22)
        with pytest.raises(
            ValueError,
            match="RANKING{은,는} 2023-12-22부터 데이터를 조회할 수 있습니다.",
        ):
            get_character_union_rank(character_name=character_name, date=date)

    # Tests error handling for future date
    def test_retrieve_with_future_date(self):
        character_name = "밥먹어친구야"
        date = kst.datetime(2099, 1, 1)
        with pytest.raises(APIError, match="Please wait until the data is ready"):
            get_character_union_rank(character_name=character_name, date=date)

    # Tests error handling for date without KST timezone info
    def test_retrieve_with_timezone_agnostic_date(self):
        character_name = "밥먹어친구야"
        date = datetime(2023, 12, 22)
        with pytest.raises(ValueError, match="datetime should have timezone info."):
            get_character_union_rank(character_name=character_name, date=date)
