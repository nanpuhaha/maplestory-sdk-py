from datetime import datetime

import pytest

from maplestory.apis.history import (
    get_account_id,
    get_cube_usage_history,
    get_potential_history,
    get_starforce_history,
    validate_count,
    validate_date_and_cursor,
)
from maplestory.error import APIError
from maplestory.models.history.potential import (
    CubeHistory,
    CubeHistoryInfo,
    PotentialHistory,
    PotentialOption,
)
from maplestory.models.history.starforce import StarforceHistory, StarforceHistoryInfo
from maplestory.utils.kst import KST_TZ
from maplestory.utils.kst import datetime as kst_datetime


class TestGetAccountId:
    # Returns a string representing the account identifier when the API call is successful
    def test_successful_api_call(self):
        # Invoke the function under test
        account_id = get_account_id()

        # Assert that the account_id is a string
        assert isinstance(account_id, str)


class TestValidateDateAndCursor:
    # Providing a valid date and cursor should not raise any exceptions.
    def test_valid_date_and_cursor_with_valid_date_and_cursor(self):
        date = datetime.now()
        cursor = "some_cursor"

        with pytest.raises(ValueError, match="date and cursor cannot be used together"):
            validate_date_and_cursor(date, cursor)

    # Providing only a valid cursor should not raise any exceptions.
    def test_valid_date_and_cursor_with_valid_cursor(self):
        cursor = "some_cursor"

        validate_date_and_cursor(date=None, cursor=cursor)

    # Providing only a valid date should not raise any exceptions.
    def test_valid_date_and_cursor_with_valid_date(self):
        date = datetime.now()

        validate_date_and_cursor(date=date, cursor=None)

    # Providing neither a date nor a cursor should raise a ValueError.
    def test_valid_date_and_cursor_with_no_date_and_cursor(self):
        with pytest.raises(ValueError):
            validate_date_and_cursor(date=None, cursor=None)

    # Providing an invalid date format should raise a ValueError.
    def test_valid_date_and_cursor_with_invalid_date_format(self):
        date = datetime.now()
        cursor = "some_cursor"

        with pytest.raises(ValueError):
            validate_date_and_cursor(date, cursor)


class TestValidateCount:
    # validate count at lower bound
    def test_valid_count_lower_bound(self):
        count = 10
        validate_count(count)

    # validate count within range
    def test_valid_count_within_range(self):
        count = 500
        validate_count(count)

    # validate count at upper bound
    def test_valid_count_upper_bound(self):
        count = 1000
        validate_count(count)

    # validate count at -1
    def test_invalid_count_negative_one(self):
        count = -1
        with pytest.raises(ValueError):
            validate_count(count)

    # validate count at 0
    def test_invalid_count_zero(self):
        count = 0
        with pytest.raises(ValueError):
            validate_count(count)

    # validate count at 1
    def test_invalid_count_one(self):
        count = 1
        with pytest.raises(ValueError):
            validate_count(count)

    # validate count at 9
    def test_invalid_count_nine(self):
        count = 9
        with pytest.raises(ValueError):
            validate_count(count)

    # validate count at 9
    def test_invalid_count_over_maximum(self):
        count = 1001
        with pytest.raises(ValueError):
            validate_count(count)

    # raises ValueError when count is not an integer
    def test_invalid_type_str(self):
        count = "abc"
        with pytest.raises(TypeError):
            validate_count(count)

        count = "500"
        with pytest.raises(TypeError):
            validate_count(count)


def test_get_cube_usage_history():
    result = get_cube_usage_history(10)
    assert isinstance(result, CubeHistory)

    # empty cube history
    result = get_cube_usage_history(10, datetime(2024, 1, 24, tzinfo=KST_TZ))
    assert isinstance(result, CubeHistory)
    assert result.count == 0
    assert result.next_cursor is None
    assert isinstance(result.history, list)
    assert len(result.history) == 0

    # 10 cube history with date
    result = get_cube_usage_history(10, datetime(2024, 1, 23, tzinfo=KST_TZ))
    assert isinstance(result, CubeHistory)
    assert result.count == 10
    assert (
        result.next_cursor
        == "82b75b3795bed5d4505866e741aff4793663933da92e7566c55104ec9ac2894d"
    )
    assert isinstance(result.history[0], CubeHistoryInfo)
    assert result.history[0].id == "QzwiJQ4l8JG3GufTs1SjE9sS"

    # 15 Cube history with page cursor
    result = get_cube_usage_history(15, page_cursor=result.next_cursor)
    assert isinstance(result, CubeHistory)
    assert result.count == 15
    assert (
        result.next_cursor
        == "44a3d34f1d722d46400f7df723583cd6e85e07f9d5d276f44440847eec04ba68"
    )
    assert isinstance(result.history[0], CubeHistoryInfo)
    assert result.history[0].id == "QzwiJQ4l8JG3GOfTs1SjF9wE"


class TestGetStarforceHistory:
    # Should return a StarforceHistory object when called with default parameters
    def test_default_parameters(self):
        result = get_starforce_history()

        assert isinstance(result, StarforceHistory)

    def test_valid_date_and_return_history(self):
        result = get_starforce_history(date=kst_datetime(2024, 2, 17))
        assert isinstance(result, StarforceHistory)
        assert result.count == 37
        assert result.next_cursor is None
        assert isinstance(result.history[0], StarforceHistoryInfo)
        starforce_history = result.history[0]
        assert (
            starforce_history.id
            == "d386a017b9ec718a2567b8e24be1fa969dcd095b4e9413f24642918d67cdc87e9bbac7677027e68e10336902d959ef23"
        )
        assert starforce_history.item_upgrade_result == "성공"
        assert starforce_history.before_starforce_count == 9
        assert starforce_history.after_starforce_count == 10
        assert starforce_history.starcatch_result == "실패/해제"
        assert starforce_history.superior_item_flag == "슈페리얼 장비 미해당"
        assert starforce_history.destroy_defense == "파괴 방지 미적용"
        assert starforce_history.chance_time == "찬스타임 미적용"
        assert starforce_history.event_field_flag == "파괴 방지 이벤트맵 미적용"
        assert starforce_history.upgrade_item == ""
        assert starforce_history.protect_shield == "프로텍트 실드 미적용/소멸되지 않음"
        assert starforce_history.bonus_stat_upgrade == "보너스 스탯 미적용 아이템"
        assert starforce_history.character_name == "귀농미인"
        assert starforce_history.world_name == "엘리시움"
        assert starforce_history.target_item == "이클레틱 파라온"
        assert starforce_history.date_create == kst_datetime(
            2024, 2, 17, 22, 22, 26, 201000
        )
        assert starforce_history.starforce_event_list is None

        result = get_starforce_history(result_count=10, date=kst_datetime(2024, 2, 17))
        assert isinstance(result, StarforceHistory)
        assert result.count == 10
        assert (
            result.next_cursor
            == "ffabe27b7ca5a561cf605029d6c1b80d3663933da92e7566c55104ec9ac2894d"
        )
        starforce_history = result.history[0]
        assert isinstance(starforce_history, StarforceHistoryInfo)
        assert (
            starforce_history.id
            == "d386a017b9ec718a2567b8e24be1fa969dcd095b4e9413f24642918d67cdc87e9bbac7677027e68e10336902d959ef23"
        )
        assert starforce_history.item_upgrade_result == "성공"
        assert starforce_history.before_starforce_count == 9
        assert starforce_history.after_starforce_count == 10
        assert starforce_history.starcatch_result == "실패/해제"
        assert starforce_history.superior_item_flag == "슈페리얼 장비 미해당"
        assert starforce_history.destroy_defense == "파괴 방지 미적용"
        assert starforce_history.chance_time == "찬스타임 미적용"
        assert starforce_history.event_field_flag == "파괴 방지 이벤트맵 미적용"
        assert starforce_history.upgrade_item == ""
        assert starforce_history.protect_shield == "프로텍트 실드 미적용/소멸되지 않음"
        assert starforce_history.bonus_stat_upgrade == "보너스 스탯 미적용 아이템"
        assert starforce_history.character_name == "귀농미인"
        assert starforce_history.world_name == "엘리시움"
        assert starforce_history.target_item == "이클레틱 파라온"
        assert starforce_history.date_create == kst_datetime(
            2024, 2, 17, 22, 22, 26, 201000
        )
        assert starforce_history.starforce_event_list is None

        result = get_starforce_history(result_count=10, page_cursor=result.next_cursor)
        assert isinstance(result, StarforceHistory)
        assert result.count == 10
        assert (
            result.next_cursor
            == "53ea968f49332fa90c402ee39ae75b80fd842dab14be2a956555625b37c97bff"
        )
        starforce_history = result.history[0]
        assert isinstance(starforce_history, StarforceHistoryInfo)
        assert (
            starforce_history.id
            == "e107df04305afa889e69dd47421de448893941c5fc308cdd0eaebf750fac8c229bbac7677027e68e10336902d959ef23"
        )
        assert starforce_history.item_upgrade_result == "성공"
        assert starforce_history.before_starforce_count == 2
        assert starforce_history.after_starforce_count == 3
        assert starforce_history.starcatch_result == "실패/해제"
        assert starforce_history.superior_item_flag == "슈페리얼 장비 미해당"
        assert starforce_history.destroy_defense == "파괴 방지 미적용"
        assert starforce_history.chance_time == "찬스타임 미적용"
        assert starforce_history.event_field_flag == "파괴 방지 이벤트맵 미적용"
        assert starforce_history.upgrade_item == ""
        assert starforce_history.protect_shield == "프로텍트 실드 미적용/소멸되지 않음"
        assert starforce_history.bonus_stat_upgrade == "보너스 스탯 미적용 아이템"
        assert starforce_history.character_name == "귀농미인"
        assert starforce_history.world_name == "엘리시움"
        assert starforce_history.target_item == "이클레틱 파라온"
        assert starforce_history.date_create == kst_datetime(
            2024, 2, 17, 22, 22, 9, 903000
        )
        assert starforce_history.starforce_event_list is None

    # Should return a StarforceHistory object when called with a valid page cursor
    def test_valid_page_cursor(self):
        result = get_starforce_history(
            result_count=10,
            page_cursor="ffabe27b7ca5a561cf605029d6c1b80d3663933da92e7566c55104ec9ac2894d",
        )
        assert isinstance(result, StarforceHistory)
        assert result.count == 10
        assert (
            result.next_cursor
            == "53ea968f49332fa90c402ee39ae75b80fd842dab14be2a956555625b37c97bff"
        )
        assert isinstance(result.history[0], StarforceHistoryInfo)

    # Should return a StarforceHistory object when called with a valid date
    def test_valid_date(self):
        result = get_starforce_history(date=kst_datetime(2023, 12, 27))

        assert isinstance(result, StarforceHistory)
        # ValueError: 스타포스{은,는} 2023-12-27부터 데이터를 조회할 수 있습니다.

    # Should return a StarforceHistory object when called with a valid date
    def test_invalid_date(self):
        with pytest.raises(
            ValueError,
            match="스타포스{은,는} 2023-12-27부터 데이터를 조회할 수 있습니다.",
        ):
            get_starforce_history(date=kst_datetime(2023, 12, 26))

    def test_invalid_date_without_timezone(self):
        with pytest.raises(ValueError, match="datetime should have timezone info."):
            get_starforce_history(date=datetime(2022, 1, 1))

    # Should raise a ValueError when called with an invalid result count less than 10
    def test_invalid_result_count_less_than_10(self):
        with pytest.raises(ValueError):
            get_starforce_history(result_count=5)

    # Should raise a ValueError when called with an invalid result count greater than 1000
    def test_invalid_result_count_greater_than_1000(self):
        with pytest.raises(ValueError):
            get_starforce_history(result_count=2000)

    def test_both_date_and_page_cursor(self):
        # date will be ignored
        next_cursor = "473ca6c580668adb33120588fd573d3686e68d4012202d0434d05f81868f68e3"
        result = get_starforce_history(
            result_count=10, page_cursor=next_cursor, date=kst_datetime(2024, 1, 2)
        )
        assert isinstance(result, StarforceHistory)
        assert result.count == 0
        assert result.next_cursor is None

        next_cursor = "ffabe27b7ca5a561cf605029d6c1b80d3663933da92e7566c55104ec9ac2894d"
        result = get_starforce_history(
            result_count=10, page_cursor=next_cursor, date=kst_datetime(2099, 12, 31)
        )
        assert isinstance(result, StarforceHistory)
        assert result.count == 10
        assert (
            result.next_cursor
            == "53ea968f49332fa90c402ee39ae75b80fd842dab14be2a956555625b37c97bff"
        )


class TestGetCubeUsageHistory:
    # Should return a CubeHistory object
    def test_return_cube_history_object(self):
        result = get_cube_usage_history(result_count=10, date=kst_datetime(2024, 1, 23))

        assert isinstance(result, CubeHistory)
        assert result.count == 10
        assert (
            result.next_cursor
            == "82b75b3795bed5d4505866e741aff4793663933da92e7566c55104ec9ac2894d"
        )
        assert isinstance(result.history, list)

    # Should return an empty CubeHistory object when given a date with no cube history
    def test_return_empty_cube_history_object(self):
        result = get_cube_usage_history(10, datetime(2024, 1, 24, tzinfo=KST_TZ))

        assert isinstance(result, CubeHistory)
        assert result.count == 0
        assert result.next_cursor is None
        assert isinstance(result.history, list)
        assert len(result.history) == 0

    # Should return a CubeHistory object with 10 history items when given a date with 10 or more cube history items
    def test_return_cube_history_with_10_items(self):
        result = get_cube_usage_history(10, datetime(2024, 1, 23, tzinfo=KST_TZ))

        assert isinstance(result, CubeHistory)
        assert result.count == 10
        assert (
            result.next_cursor
            == "82b75b3795bed5d4505866e741aff4793663933da92e7566c55104ec9ac2894d"
        )
        assert isinstance(result.history, list)
        assert len(result.history) == 10
        assert isinstance(result.history[0], CubeHistoryInfo)
        assert result.history[0].id == "QzwiJQ4l8JG3GufTs1SjE9sS"
        cube_history = result.history[0]
        assert cube_history.id == "QzwiJQ4l8JG3GufTs1SjE9sS"
        assert cube_history.character_name == "귀농남친"
        assert cube_history.date_create == kst_datetime(2024, 1, 23, 21, 56, 29, 737000)
        assert cube_history.cube_type == "수상한 에디셔널 큐브"
        assert cube_history.item_upgrade_result == "실패"
        assert cube_history.miracle_time_flag == "이벤트 적용되지 않음"
        assert cube_history.item_equipment_part == "보조무기"
        assert cube_history.item_level == 100
        assert cube_history.target_item == "에레브의 광휘"
        assert cube_history.potential_option_grade == "에픽"
        assert cube_history.additional_potential_option_grade == "에픽"
        assert cube_history.upgrade_guarantee is False
        assert cube_history.upgrade_guarantee_count == 0
        assert cube_history.before_potential_option == []
        assert cube_history.before_additional_potential_option == [
            PotentialOption(value="최대 HP : +5%", grade="에픽"),
            PotentialOption(value="방어력 : +100", grade="레어"),
            PotentialOption(value="최대 MP : +2%", grade="레어"),
        ]
        assert cube_history.after_potential_option == []
        assert cube_history.after_additional_potential_option == [
            PotentialOption(value="데미지 : +6%", grade="에픽"),
            PotentialOption(value="최대 MP : +2%", grade="레어"),
            PotentialOption(value="최대 HP : +100", grade="레어"),
        ]

    # Should raise a ValueError when page cursor is invalid
    def test_raise_value_error_when_invalid_page_cursor_provided(self):
        with pytest.raises(APIError, match="Please input valid id"):
            get_cube_usage_history(page_cursor="cursor")

    # Should raise a ValueError when both date and page cursor are provided
    def test_raise_value_error_when_both_date_and_page_cursor_provided(self):
        # date will be ignored
        result = get_cube_usage_history(
            10,
            datetime(1999, 1, 1, tzinfo=KST_TZ),
            page_cursor="82b75b3795bed5d4505866e741aff4793663933da92e7566c55104ec9ac2894d",
        )
        assert isinstance(result.history, list)
        assert len(result.history) == 10
        cube_history = result.history[0]
        assert isinstance(cube_history, CubeHistoryInfo)
        assert cube_history.id == "QzwiJQ4l8JG3GOfTs1SjF9wE"
        assert cube_history.character_name == "귀농남친"
        assert cube_history.date_create == kst_datetime(2024, 1, 23, 21, 56, 8, 819000)
        assert cube_history.cube_type == "수상한 에디셔널 큐브"
        assert cube_history.item_upgrade_result == "실패"
        assert cube_history.miracle_time_flag == "이벤트 적용되지 않음"
        assert cube_history.item_equipment_part == "보조무기"
        assert cube_history.item_level == 100
        assert cube_history.target_item == "에레브의 광휘"
        assert cube_history.potential_option_grade == "에픽"
        assert cube_history.additional_potential_option_grade == "레어"
        assert cube_history.upgrade_guarantee is False
        assert cube_history.upgrade_guarantee_count == 0
        assert cube_history.before_potential_option == []
        assert cube_history.before_additional_potential_option == [
            PotentialOption(value="최대 HP : +100", grade="레어"),
            PotentialOption(value="DEX : +6", grade="노멀"),
            PotentialOption(value="최대 HP : +50", grade="노멀"),
        ]
        assert cube_history.after_potential_option == []
        assert cube_history.after_additional_potential_option == [
            PotentialOption(value="이동속도 : +5", grade="레어"),
            PotentialOption(value="방어력 : +50", grade="노멀"),
            PotentialOption(value="최대 HP : +50", grade="노멀"),
        ]

    # Should raise a ValueError when neither date nor page cursor are provided
    def test_raise_value_error_when_neither_date_nor_page_cursor_provided(self):
        with pytest.raises(ValueError):
            get_cube_usage_history(10, date=None, page_cursor=None)

    # Should raise a ValueError when result_count is less than 10
    def test_raise_value_error_when_result_count_less_than_10(self):
        with pytest.raises(ValueError):
            get_cube_usage_history(5)


class TestGetPotentialHistory:
    # Should return a PotentialHistory object with count, next_cursor and history attributes when called with default arguments
    def test_default_arguments(self):
        result = get_potential_history()
        assert isinstance(result, PotentialHistory)

    def test_minimum_count(self):
        result = get_potential_history(10)
        assert isinstance(result, PotentialHistory)

    # Should raise a ValueError when called with count less than 10
    def test_invalid_count_less_than_10(self):
        with pytest.raises(ValueError):
            get_potential_history(result_count=5)

    # Should raise a ValueError when called with count greater than 1000
    def test_invalid_count_greater_than_1000(self):
        with pytest.raises(ValueError):
            get_potential_history(result_count=2000)

    def test_raise_value_error_without_timezone(self):
        with pytest.raises(ValueError, match="datetime should have timezone info."):
            get_potential_history(date=datetime(2022, 1, 1))

    def test_with_invalid_date(self):
        with pytest.raises(
            ValueError,
            match="잠재능력{은,는} 2024-01-25부터 데이터를 조회할 수 있습니다.",
        ):
            get_potential_history(date=kst_datetime(2022, 1, 1))

    # Should return a PotentialHistory object with empty history list when called with a date that has no data
    def test_no_data_date(self):
        result = get_potential_history(date=kst_datetime(2024, 1, 25))

        assert isinstance(result, PotentialHistory)
        assert result.count == 0
        assert result.next_cursor is None
        assert result.history == []

    def test_with_datetime_with_timezone(self):
        result = get_potential_history(date=datetime(2024, 2, 17, tzinfo=KST_TZ))
        result2 = get_potential_history(date=kst_datetime(2024, 2, 17))
        assert result == result2

    # Should return a PotentialHistory object with history list when called with a date that has data
    def test_with_data_date(self):
        result = get_potential_history(date=kst_datetime(2024, 2, 17))

        assert isinstance(result, PotentialHistory)
        assert result.count == 13
        assert result.next_cursor is None
        assert len(result.history) == 13

        history_item = result.history[0]

        assert history_item.id == "QzwlKQ4m8JG3HOfTs1yhE-6P"
        assert history_item.character_name == "귀농미인"
        assert history_item.date_create == kst_datetime(2024, 2, 17, 22, 35, 7, 112000)
        assert history_item.potential_type == "잠재능력 재설정"
        assert history_item.item_upgrade_result == "실패"
        assert history_item.miracle_time_flag == "이벤트 적용되지 않음"
        assert history_item.item_equipment_part == "신발"
        assert history_item.item_level == 120.0
        assert history_item.target_item == "이클레틱 파라온"
        assert history_item.potential_option_grade == "레어"
        assert history_item.additional_potential_option_grade == "노멀"
        assert history_item.upgrade_guarantee is False
        assert history_item.upgrade_guarantee_count == 2.0
        assert history_item.before_potential_option == [
            PotentialOption(value="최대 HP : +3%", grade="레어"),
            PotentialOption(value="최대 MP : +60", grade="노멀"),
            PotentialOption(value="점프력 : +4", grade="노멀"),
        ]
        assert history_item.after_potential_option == [
            PotentialOption(value="방어력 : +3%", grade="레어"),
            PotentialOption(value="방어력 : +3%", grade="레어"),
            PotentialOption(value="DEX : +6", grade="노멀"),
        ]
        assert history_item.before_additional_potential_option == []
        assert history_item.after_additional_potential_option == []

    # Should raise a ValueError when called with both date and cursor arguments
    def test_invalid_arguments_date_and_cursor(self):
        with pytest.raises(APIError, match="Please input valid id"):
            get_potential_history(date=datetime(2022, 1, 1), page_cursor="abc123")
