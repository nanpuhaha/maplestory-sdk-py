from datetime import datetime

from pydantic import BaseModel, Field


class Popularity(BaseModel):
    """캐릭터 인기도 정보

    Attributes:
        date (datetime): 조회 기준일
        popularity (int): 인기도
    """

    date: datetime = Field(repr=False)
    popularity: int
