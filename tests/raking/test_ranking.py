# from rich import print
# import maplestory.utils.kst as kst
# from maplestory.apis.ranking import (
#     get_overall_ranking, get_union_ranking, get_guild_ranking, get_dojang_ranking, get_theseed_ranking, get_achievement_ranking
# )

# TEST_GUILDS = [("리더", "스카니아"), ("좋은부자", "엘리시움")]

# @pytest.mark.parametrize("guild_name,world_name", TEST_GUILDS)
# def test_get_id(guild_name: str, world_name: str):
#     guild_id = get_guild_id(guild_name, world_name)
#     print(f"{guild_name = }, {world_name = } -> {guild_id = }")
#     assert isinstance(guild_id, str)
    
# @pytest.mark.parametrize("guild_name,world_name", [("리더", "스카니아"), ("좋은부자", "엘리시움")])
# def test_get_overall_ranking(
#     result = get_overall_ranking(world_name="스카니아", character_id: str | None = None, page_number: int = 1, date: kst.datetime(2024, 1, 1))
#     assert isinstance(result, OverallRanking)






# def test_get_overall_ranking(
#     result = get_overall_ranking(world_name="스카니아", character_id: str | None = None, page_number: int = 1, date: kst.datetime(2024, 1, 1))
#     assert isinstance(result, OverallRanking)

# def test_get_union_ranking(
#     result = get_union_ranking(world: UnionWorldName | None = None, character_id: str | None = None, page_number: int = 1, date: kst.KSTdatetime = kst.yesterday)
#     assert isinstance(result, UnionRanking)

# def test_get_guild_ranking(
#     result = get_guild_ranking(ranking_type: int | GuildRankType = GuildRankType.주간명성치, world_name: WorldName | None = None, guild: str | None = None, page_number: int = 1, date: kst.KSTdatetime = kst.yesterday)
#     assert isinstance(result, GuildRanking)

# def test_get_dojang_ranking(
#     result = get_dojang_ranking(world_name: str | None = None, job_class: JobClass | None = None, character_id: str | None = None, page_number: int = 1, difficulty_level: int | DojangDifficulty = DojangDifficulty.통달, date: kst.AwareDatetime = kst.yesterday)
#     assert isinstance(result, DojangRanking)

# def test_get_theseed_ranking(
#     result = get_theseed_ranking(world_name: WorldName | None = None, character_id: str | None = None, page_number: int = 1, date: kst.AwareDatetime = kst.yesterday)
#     assert isinstance(result, TheSeedRanking)

# def test_get_achievement_ranking(
#     result = get_achievement_ranking(character_id: str | None = None, page_number: int = 1, date: kst.AwareDatetime = kst.yesterday)
#     assert isinstance(result, AchievementRanking)
