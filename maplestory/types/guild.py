from typing import Annotated, Literal

from annotated_types import Ge, Le

GuildLevel = Annotated[int, Ge(1), Le(30)]
GuildRankType = Literal["weekly_fame", "flag_race", "sewer"]
