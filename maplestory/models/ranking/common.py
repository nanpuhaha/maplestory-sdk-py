from typing import Any, Generic, TypeVar

from pydantic import BaseModel

RankingInfoType = TypeVar("RankingInfoType")


class RankingModel(BaseModel, Generic[RankingInfoType]):
    """랭킹 모델의 기본 클래스

    Attributes:
        ranking: 랭킹 목록
    """

    ranking: list[RankingInfoType]

    def model_post_init(self, __context: Any) -> None:
        self.ranking = sorted(self.ranking, key=lambda x: x.ranking)

    def __iter__(self):
        return iter(self.ranking)

    def __getitem__(self, index: int) -> RankingInfoType:
        return self.ranking[index]

    def __len__(self) -> int:
        return len(self.ranking)
