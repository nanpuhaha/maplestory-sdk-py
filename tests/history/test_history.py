from datetime import datetime

import pytest
from rich import print

from maplestory.apis.history import (
    get_account_id,
    get_cube_usage_history,
    get_potential_history,
    get_starforce_history,
    validate_count,
    validate_date_and_cursor,
)
from maplestory.models.history.potential import (
    CubeHistory,
    CubeHistoryInfo,
    PotentialHistory,
)
from maplestory.models.history.starforce import StarforceHistory
from maplestory.utils.kst import KST_TZ


def test_get_account_id():
    account_id = get_account_id()
    print(f"{account_id = }")
    assert isinstance(account_id, str)


def test_valid_date_and_cursor():
    # 유효한 date와 cursor 값이 주어진 경우 예외가 발생하지 않아야 합니다.

    # cursor만 주어지는 경우
    assert validate_date_and_cursor(date=None, cursor="some_cursor") is None

    # date만 주어지는 경우
    assert validate_date_and_cursor(date=datetime.now(), cursor=None) is None


def test_invalid_date_and_cursor():
    # date와 cursor가 동시에 주어지면 ValueError 예외가 발생해야 합니다.
    with pytest.raises(ValueError):
        validate_date_and_cursor(date=datetime.now(), cursor="some_cursor")

    # date와 cursor 둘 다 주어지지 않으면 ValueError 예외가 발생해야 합니다.
    with pytest.raises(ValueError):
        validate_date_and_cursor(date=None, cursor=None)


def test_valid_count():
    # validate count at lower bound
    count = 10
    assert validate_count(count) is None

    # validate count within range
    count = 500
    assert validate_count(count) is None

    # validate count at upper bound
    count = 1000
    assert validate_count(count) is None


def test_invalid_count():
    count = -1
    with pytest.raises(ValueError):
        validate_count(count)

    count = 0
    with pytest.raises(ValueError):
        validate_count(count)

    count = 1
    with pytest.raises(ValueError):
        validate_count(count)

    count = 9
    with pytest.raises(ValueError):
        validate_count(count)

    count = 1001
    with pytest.raises(ValueError):
        validate_count(count)

    # raises ValueError when count is not an integer
    count = "abc"
    with pytest.raises(TypeError):
        validate_count(count)

    # raises ValueError when count is not an integer
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


def test_get_starforce_history():
    result = get_starforce_history(10)
    print(result)
    assert isinstance(result, StarforceHistory)


def test_get_potential_history():
    result = get_potential_history(10)
    print(result)
    assert isinstance(result, PotentialHistory)

    result = get_potential_history(10, datetime(2024, 1, 25, tzinfo=KST_TZ))
    assert isinstance(result, PotentialHistory)
    assert result.count == 0
    assert result.next_cursor is None
    assert isinstance(result.history, list)
    assert len(result.history) == 0
