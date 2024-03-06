import sys

import pytest

import maplestory.utils.kst as kst
from maplestory.enums import NormalWorld, RebootWorld
from maplestory.error import APIError
from maplestory.models.ranking.overall import OverallRanking, OverallRankingInfo
from maplestory.services.rankings.overall import (
    get_character_overall_rank,
    get_job_class_overall_ranking,
    get_normal_world_overall_ranking,
    get_overall_ranking,
    get_reboot_world_overall_ranking,
    get_world_overall_ranking,
)


class TestGetOverallRanking:
    # Tests retrieving OverallRanking with all valid parameters specified
    def test_retrieve_with_all_valid_parameters(self):
        world_name = "스카니아"
        job_class = "전사-히어로"
        page_number = 1
        date = kst.yesterday()

        ranking = get_overall_ranking(
            world_name=world_name,
            job_class=job_class,
            page_number=page_number,
            date=date,
        )
        first_rank = ranking[0]

        assert isinstance(ranking, OverallRanking)
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 1
        assert first_rank.world_name == world_name
        assert first_rank.class_name == "전사"
        assert first_rank.sub_class_name == "히어로"
        assert first_rank.date == date

    # Tests the response when an invalid world name is provided
    def test_retrieve_with_invalid_world_name(self):
        world_name = "InvalidWorld"
        job_class = "전사-히어로"
        page_number = 1
        date = kst.yesterday()

        ranking = get_overall_ranking(
            world_name=world_name,
            job_class=job_class,
            page_number=page_number,
            date=date,
        )

        assert isinstance(ranking, OverallRanking)
        assert len(ranking) == 0

    # Tests retrieving OverallRanking by specifying only the page number
    def test_retrieve_with_only_page_number(self):
        page_number = 1

        ranking = get_overall_ranking(page_number=page_number)
        first_rank = ranking[0]

        assert isinstance(ranking, OverallRanking)
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 1
        assert first_rank.date == kst.yesterday()

    # Tests retrieving OverallRanking by specifying only the date
    def test_retrieve_with_only_date(self):
        date = kst.yesterday()

        ranking = get_overall_ranking(date=date)
        first_rank = ranking[0]

        assert isinstance(ranking, OverallRanking)
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 1
        assert first_rank.date == date


class TestGetNormalWorldOverallRanking:
    # Tests retrieving overall ranking for a normal world using default parameters
    def test_default_parameters_normal_world(self):
        ranking = get_normal_world_overall_ranking()
        first_rank = ranking[0]

        assert isinstance(ranking, OverallRanking)
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 1
        assert first_rank.date == kst.yesterday()
        if sys.version_info >= (3, 12):
            assert first_rank.world_name in NormalWorld
        else:
            assert first_rank.world_name in NormalWorld.values()

    # Tests retrieving overall ranking for a normal world with specific job class, page number, and date
    def test_specific_parameters_normal_world(self):
        job_class = "전사-전체 전직"
        page_number = 2
        date = kst.datetime(2023, 12, 22, 8, 30)

        ranking = get_normal_world_overall_ranking(
            job_class=job_class, page_number=page_number, date=date
        )
        first_rank = ranking[0]

        assert isinstance(ranking, OverallRanking)
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 201  # Assuming a specific ranking for this test
        assert first_rank.class_name == "전사"
        assert kst.is_same_date(first_rank.date, date)
        if sys.version_info >= (3, 12):
            assert first_rank.world_name in NormalWorld
        else:
            assert first_rank.world_name in NormalWorld.values()

    # Tests error handling when an invalid job class is provided
    def test_invalid_job_class_normal_world(self):
        job_class = "InvalidJobClass"
        with pytest.raises(APIError, match="Please input valid parameter"):
            get_normal_world_overall_ranking(job_class=job_class)

    # Tests error handling for a negative page number
    def test_negative_page_number_normal_world(self):
        page_number = -1
        with pytest.raises(APIError, match="Please input valid parameter"):
            get_normal_world_overall_ranking(page_number=page_number)


class TestGetRebootWorldOverallRanking:
    # Tests retrieving overall ranking for a reboot world using default parameters
    def test_default_parameters_reboot_world(self):
        ranking = get_reboot_world_overall_ranking()
        first_rank = ranking[0]

        assert isinstance(ranking, OverallRanking)
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 1
        assert first_rank.date == kst.yesterday()
        if sys.version_info >= (3, 12):
            assert first_rank.world_name in RebootWorld
        else:
            assert first_rank.world_name in RebootWorld.values()

    # Tests retrieving overall ranking for a reboot world with specific parameters
    def test_specific_parameters_reboot_world(self):
        job_class = "전사-히어로"
        page_number = 1
        date = kst.yesterday()

        ranking = get_reboot_world_overall_ranking(
            job_class=job_class, page_number=page_number, date=date
        )
        first_rank = ranking[0]

        assert isinstance(ranking, OverallRanking)
        assert ranking.world_names <= {"리부트", "리부트2"}
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 1
        assert first_rank.class_name == "전사"
        assert first_rank.sub_class_name == "히어로"
        assert first_rank.date == kst.yesterday()
        if sys.version_info >= (3, 12):
            assert first_rank.world_name in RebootWorld
        else:
            assert first_rank.world_name in RebootWorld.values()

    # Tests error handling for a non-existent job class in a reboot world
    def test_nonexistent_job_class_reboot_world(self):
        job_class = "InvalidJobClass"
        with pytest.raises(APIError, match="Please input valid parameter"):
            get_reboot_world_overall_ranking(job_class=job_class)

    # Tests error handling for a negative page number in a reboot world
    def test_negative_page_number_reboot_world(self):
        page_number = -1
        with pytest.raises(APIError, match="Please input valid parameter"):
            get_reboot_world_overall_ranking(page_number=page_number)


class TestGetWorldOverallRanking:
    # Tests retrieving the overall ranking for a specific world using default parameters
    def test_retrieve_default_for_world(self):
        world_name = "스카니아"
        ranking = get_world_overall_ranking(world_name)
        first_rank = ranking[0]
        assert isinstance(ranking, OverallRanking)
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 1
        assert first_rank.world_name == world_name
        assert first_rank.date == kst.yesterday()

    # Tests retrieving the overall ranking for a specific world with all provided parameters
    def test_retrieve_specific_world_with_all_params(self):
        world_name = "스카니아"
        job_class = "전사-히어로"
        page_number = 2
        date = kst.yesterday()
        ranking = get_world_overall_ranking(world_name, job_class, page_number, date)
        first_rank = ranking[0]
        assert isinstance(ranking, OverallRanking)
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 201
        assert first_rank.world_name == world_name
        assert first_rank.date == date
        assert first_rank.class_name == "전사"
        assert first_rank.sub_class_name == "히어로"

    # Tests attempting to retrieve the overall ranking for a nonexistent world
    def test_nonexistent_world_name(self):
        world_name = "Nonexistent World"
        ranking = get_world_overall_ranking(world_name)
        assert isinstance(ranking, OverallRanking)
        assert len(ranking) == 0


class TestGetJobClassOverallRanking:
    # Tests retrieving the overall ranking for a specific job class using default parameters
    def test_retrieve_default_for_job_class(self):
        job_class = "전사-히어로"
        ranking = get_job_class_overall_ranking(job_class)
        first_rank = ranking[0]
        assert isinstance(ranking, OverallRanking)
        assert isinstance(first_rank, OverallRankingInfo)
        assert first_rank.ranking == 1
        assert first_rank.class_name == "전사"
        assert first_rank.sub_class_name == "히어로"
        assert first_rank.date == kst.yesterday()

    # Tests retrieving the overall ranking for a job class that does not exist or is not specified
    def test_nonexistent_or_unspecified_job_class(self):
        job_class = None
        ranking = get_job_class_overall_ranking(job_class)
        first_rank = ranking[0]
        assert isinstance(ranking, OverallRanking)
        assert first_rank.ranking == 1
        assert first_rank.date == kst.yesterday()


class TestGetCharacterOverallRank:
    # Tests retrieving OverallRankingInfo for a character with a valid name using the default date
    def test_retrieve_for_valid_character_with_default_date(self):
        character_name = "온앤온"
        rank = get_character_overall_rank(character_name=character_name)
        assert isinstance(rank, OverallRankingInfo)
        assert rank.date == kst.yesterday()
        assert rank.character_name == character_name

    # Tests error handling for an invalid or nonexistent character name
    def test_error_handling_for_invalid_character_name(self):
        character_name = "InvalidCharacter"
        with pytest.raises(APIError, match="Please input valid parameter"):
            get_character_overall_rank(character_name=character_name)

    # Tests retrieving OverallRankingInfo when no data is available for the given character and date
    def test_retrieve_when_no_data_available_for_date(self):
        character_name = "로청사줘"
        date = kst.datetime(2023, 12, 22)  # A date before the character's creation
        rank = get_character_overall_rank(character_name=character_name, date=date)
        assert rank is None
