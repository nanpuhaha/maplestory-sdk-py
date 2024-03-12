from datetime import datetime, timedelta

import pytest

from maplestory.config import Config
from maplestory.services.character import get_character_id


@pytest.fixture
def open_api_key() -> str:
    settings = Config()
    return settings.key


@pytest.fixture(params=[0, 1, 2])
def date_str(request) -> str:
    date = datetime.now() - timedelta(days=request.param)
    return date.strftime("%Y-%m-%d")


@pytest.fixture(
    params=[
        "아델",
        "온앤온",
        # "좋은부자",
        "르샹쥬",
        # "르투이쇼",
        # "르샤뜨",
        # "차별인맥",
        # "디삐컬",
        # "한용본",
        # "맥부자",
        # "나의소중한님",
        # "귀농미인카데",
    ]
)
def character_name(request):
    print(f"{request.param!r}")
    return request.param


@pytest.fixture(params=["뷁뷁"])
def invalid_character_name(request):
    print(f"{request.param!r}")
    return request.param


@pytest.fixture
def character_ocid(character_name: str) -> str:
    print(f"{character_name = }")
    return get_character_id(character_name)


@pytest.fixture(
    params=[
        "0",
        "1",
        "1.5",
        "2",
        "2.5",
        "3",
        "4",
        "hyperpassive",
        "hyperactive",
        "5",
        "6",
    ]
)
def skill_grade(request) -> str:
    print(f"skill_grade = {request.param!r}")
    return request.param
