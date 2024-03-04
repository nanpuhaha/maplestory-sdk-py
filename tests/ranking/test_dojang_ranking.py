import pytest

import maplestory.utils.kst as kst
from maplestory.enums import DojangDifficultyEnum
from maplestory.error import APIError
from maplestory.models.ranking.dojang import DojangRanking, DojangRankingInfo
from maplestory.services.rankings.dojang import (
    get_character_dojang_rank,
    get_dojang_ranking,
    get_job_class_dojang_ranking,
    get_world_dojang_ranking,
)


class TestGetDojangRanking:
    # Tests retrieving Dojang ranking for a character given valid world name, job class, and character name
    def test_retrieve_ranking_for_valid_character(self):
        # Setup test data
        world_name = "루나"
        job_class = "기사단-소울마스터"
        character_name = "밀크쌀과자"
        page_number = 1
        difficulty_level = DojangDifficultyEnum.NOVICE
        date = kst.datetime(2024, 2, 27)

        # Execute function under test
        ranking = get_dojang_ranking(
            world_name=world_name,
            job_class=job_class,
            character_name=character_name,
            page_number=page_number,
            difficulty_level=difficulty_level,
            date=date,
        )
        rank = ranking[0]

        # Verify the results
        assert isinstance(ranking, DojangRanking)
        assert isinstance(rank, DojangRankingInfo)
        assert rank.character_name == character_name
        assert rank.class_name == "기사단"
        assert rank.sub_class_name == "소울마스터"
        assert rank.world_name == world_name
        assert rank.ranking == 1
        assert rank.date == date
        assert rank.difficulty == difficulty_level
        assert rank.character_level == 200
        assert rank.floor == 38
        assert rank.time_record == 722
        assert rank.record == "12분 02초"

    # Tests that no ranking is returned for an invalid world name
    def test_retrieve_ranking_with_invalid_world_name(self):
        world_name = "InvalidWorld"

        # Execute function under test
        result = get_dojang_ranking(world_name=world_name)

        # Verify the result is empty
        assert isinstance(result, DojangRanking)
        assert len(result) == 0

    # Tests that no ranking is returned for an invalid world name even when other parameters are valid
    def test_retrieve_ranking_with_invalid_world_and_valid_others(self):
        # Setup test data with an invalid world name
        world_name = "InvalidWorld"
        job_class = "기사단-소울마스터"
        character_name = "밀크쌀과자"
        page_number = 1
        difficulty_level = DojangDifficultyEnum.NOVICE
        date = kst.datetime(2024, 2, 27)

        # Execute function under test
        result = get_dojang_ranking(
            world_name=world_name,
            job_class=job_class,
            character_name=character_name,
            page_number=page_number,
            difficulty_level=difficulty_level,
            date=date,
        )

        # Verify no ranking is returned
        assert isinstance(result, DojangRanking)
        assert len(result) == 0


class TestGetWorldDojangRanking:
    # Tests retrieving Dojang ranking for a specific world using default parameters
    def test_default_parameters(self):
        world_name = "스카니아"
        ranking = get_world_dojang_ranking(world_name)
        rank = ranking[0]
        assert isinstance(ranking, DojangRanking)
        assert rank.world_name == world_name
        assert rank.ranking == 1
        assert rank.date == kst.yesterday()
        assert rank.difficulty == DojangDifficultyEnum.MASTER

    # Tests retrieving Dojang ranking for a specific world and date
    def test_specific_world_and_date(self):
        world_name = "스카니아"
        date = kst.datetime(2024, 2, 27)

        ranking = get_world_dojang_ranking(world_name=world_name, date=date)
        rank = ranking[0]

        assert isinstance(ranking, DojangRanking)
        assert isinstance(rank, DojangRankingInfo)
        assert rank.character_name == "썰곰"
        assert rank.class_name == "기사단"
        assert rank.sub_class_name == "윈드브레이커"
        assert rank.world_name == world_name
        assert rank.ranking == 1
        assert rank.date == date
        assert rank.difficulty == DojangDifficultyEnum.MASTER
        assert rank.character_level == 289
        assert rank.floor == 91
        assert rank.time_record == 874

    # Tests retrieving Dojang ranking with all parameters specified
    def test_all_parameters_specified(self):
        world_name = "스카니아"
        job_class = "기사단-전체 전직"
        page_number = 1
        difficulty_level = DojangDifficultyEnum.NOVICE
        date = kst.datetime(2024, 2, 25)

        ranking = get_world_dojang_ranking(
            world_name=world_name,
            job_class=job_class,
            page_number=page_number,
            difficulty_level=difficulty_level,
            date=date,
        )
        rank = ranking[0]

        assert isinstance(ranking, DojangRanking)
        assert isinstance(rank, DojangRankingInfo)
        assert rank.date == date
        assert rank.ranking == 1
        assert rank.character_name == "으익으악으익"
        assert rank.world_name == world_name
        assert rank.class_name == "기사단"
        assert rank.sub_class_name == "소울마스터"
        assert rank.character_level == 200
        assert rank.floor == 35
        assert rank.time_record == 462
        assert rank.difficulty == difficulty_level
        assert rank.record == "07분 42초"

    # Tests retrieving Dojang ranking for a non-existent world
    def test_nonexistent_world(self):
        world_name = "nonexistent_world"

        result = get_world_dojang_ranking(world_name)

        assert isinstance(result, DojangRanking)
        assert len(result) == 0

    # Tests retrieving Dojang ranking with an invalid date
    def test_invalid_date_raises_error(self):
        world_name = "스카니아"
        date = kst.datetime(2023, 12, 21)

        with pytest.raises(
            ValueError,
            match="RANKING{은,는} 2023-12-22부터 데이터를 조회할 수 있습니다.",
        ):
            get_world_dojang_ranking(world_name=world_name, date=date)


class TestGetJobClassDojangRanking:
    # Tests retrieving Dojang ranking for a specific job class with default parameters
    def test_valid_job_class_default_parameters(self):
        job_class = "전사-히어로"

        ranking = get_job_class_dojang_ranking(job_class=job_class)
        rank = ranking[0]

        assert isinstance(ranking, DojangRanking)
        assert isinstance(rank, DojangRankingInfo)
        assert rank.date == kst.yesterday()
        assert rank.ranking == 1
        assert rank.class_name == "전사"
        assert rank.sub_class_name == "히어로"
        assert rank.difficulty == DojangDifficultyEnum.MASTER

    # Tests retrieving Dojang ranking with all parameters specified for a job class
    def test_all_parameters_for_job_class(self):
        job_class = "전사-히어로"
        page_number = 1
        difficulty_level = DojangDifficultyEnum.NOVICE
        date = kst.datetime(2024, 2, 27)

        ranking = get_job_class_dojang_ranking(
            job_class=job_class,
            page_number=page_number,
            difficulty_level=difficulty_level,
            date=date,
        )
        rank = ranking[0]

        assert isinstance(ranking, DojangRanking)
        assert isinstance(rank, DojangRankingInfo)
        assert rank.date == date
        assert rank.ranking == 1
        assert rank.character_name == "두근두근어로"
        assert rank.world_name == "베라"
        assert rank.class_name == "전사"
        assert rank.sub_class_name == "히어로"
        assert rank.character_level == 200
        assert rank.floor == 38
        assert rank.time_record == 839
        assert rank.difficulty == difficulty_level
        assert rank.record == "13분 59초"

    # Tests error handling for invalid job class
    def test_error_invalid_job_class(self):
        job_class = "InvalidJobClass"

        with pytest.raises(APIError, match="Please input valid parameter"):
            get_job_class_dojang_ranking(job_class=job_class)


class TestGetCharacterDojangRank:
    # Tests retrieving DojangRankingInfo for a valid character, difficulty, and date
    def test_valid_character_difficulty_and_date(self):
        character_name = "고릴라"
        difficulty_level = DojangDifficultyEnum.통달
        date = kst.datetime(2024, 2, 27)

        result = get_character_dojang_rank(
            character_name=character_name, difficulty_level=difficulty_level, date=date
        )

        assert isinstance(result, DojangRankingInfo)
        assert result.date == date
        assert result.character_name == character_name
        assert result.ranking == 1
        assert result.world_name == "루나"
        assert result.class_name == "레지스탕스"
        assert result.sub_class_name == ""
        assert result.character_level == 288
        assert result.floor == 95
        assert result.time_record == 872
        assert result.difficulty == difficulty_level

    # Tests error handling for an invalid character name
    def test_error_invalid_character_name(self):
        character_name = "NotExistentCharacter"

        with pytest.raises(APIError, match="Please input valid parameter"):
            get_character_dojang_rank(character_name=character_name)

    # Tests returning None when no ranking information is available
    def test_no_ranking_information_available(self):
        character_name = "온앤온"
        difficulty_level = DojangDifficultyEnum.통달
        date = kst.datetime(2024, 1, 1)

        result = get_character_dojang_rank(
            character_name=character_name, difficulty_level=difficulty_level, date=date
        )

        assert result is None
