from datetime import datetime

import httpx
import pytest

from maplestory.apis.union import (
    get_union_artifact_info_by_ocid,
    get_union_info_by_ocid,
    get_union_raider_info_by_ocid,
)
from maplestory.models.union.artifact import (
    UnionArtifact,
    UnionArtifactCrystal,
    UnionArtifactEffect,
)
from maplestory.models.union.raider import UnionRaider
from maplestory.models.union.union import UnionInfo
from maplestory.services.union import (
    Union,
    UnionStat,
    UnionStats,
    get_union_artifact_info,
    get_union_info,
    get_union_raider_info,
)
from maplestory.utils.kst import KST_TZ, yesterday


def test_get_union_info_by_ocid(character_ocid: str):
    result = get_union_info_by_ocid(character_ocid)
    assert isinstance(result, UnionInfo)


def test_get_union_info(character_name: str):
    result = get_union_info(character_name)
    assert isinstance(result, UnionInfo)


def test_get_union_raider_info_by_ocid(character_ocid: str):
    result = get_union_raider_info_by_ocid(character_ocid)
    assert isinstance(result, UnionRaider)


def test_get_union_raider_info(character_name: str):
    result = get_union_raider_info(character_name)
    assert isinstance(result, UnionRaider)


def test_get_union_artifact_info_by_ocid(character_ocid: str):
    result = get_union_artifact_info_by_ocid(character_ocid)
    assert isinstance(result, UnionArtifact)


def test_get_union_artifact_info(character_name: str):
    result = get_union_artifact_info(character_name)
    assert isinstance(result, UnionArtifact)


def custom_side_effect(url, params, headers, *args, **kwargs):
    if "/maplestory/v1/id" in url:
        return httpx.Response(
            200,
            json={"ocid": "562462037a5f3a4ef5085546bd0c7dd9"},
            request=httpx.Request(
                "GET",
                "https://open.api.nexon.com/maplestory/v1/id",
                params=params,
                headers=headers,
            ),
        )
    elif "/maplestory/v1/character/basic" in url:
        return httpx.Response(
            200,
            json={"oguild_id": "9c64f32a53218b692a2360b4616fc15c"},
            request=httpx.Request(
                "GET",
                "https://open.api.nexon.com/maplestory/v1/character/basic",
                params=params,
                headers=headers,
            ),
        )
    elif "/user/union-raider" in url:
        return httpx.Response(
            200,
            json={
                "date": "2024-02-21T00:00+09:00",
                "union_raider_stat": [
                    "상태 이상 내성 4 증가",
                    "INT 100 증가",
                    "DEX 100 증가",
                    "LUK 80 증가",
                    "STR 80 증가",
                    "LUK 80 증가",
                    "LUK 80 증가",
                    "적 공격마다 70%의 확률로 순수 MP의 8% 회복",
                    "DEX 100 증가",
                    "버프 지속시간 20% 증가",
                    "INT 80 증가",
                    "LUK 80 증가",
                    "STR 80 증가",
                    "STR 80 증가",
                    "INT 80 증가",
                    "INT 80 증가",
                    "STR 80 증가",
                    "경험치 획득량 10% 증가",
                    "DEX 80 증가",
                    "LUK 80 증가",
                    "STR, DEX, LUK 40 증가",
                    "크리티컬 확률 4% 증가",
                    "메소 획득량 4% 증가",
                    "INT 80 증가",
                    "INT 80 증가",
                    "보스 몬스터 공격 시 데미지 5% 증가",
                    "공격 시 20%의 확률로 데미지 16% 증가",
                    "공격력/마력 20 증가",
                    "INT 80 증가",
                    "방어율 무시 5% 증가",
                    "크리티컬 확률 4% 증가",
                    "크리티컬 데미지 5% 증가",
                    "INT 80 증가",
                    "스킬 재사용 대기시간 5% 감소",
                    "최대 MP 6% 증가",
                    "STR 80 증가",
                ],
                "union_occupied_stat": [
                    "크리티컬 데미지 20.00% 증가",
                    "마력 5 증가",
                    "LUK 5 증가",
                    "크리티컬 확률 11% 증가",
                    "보스 몬스터 공격 시 데미지 23% 증가",
                    "INT 25 증가",
                    "버프 지속시간 40% 증가",
                    "방어율 무시 33% 증가",
                ],
                "union_block": [
                    {
                        "block_type": "마법사",
                        "block_class": "아크메이지(썬,콜)",
                        "block_level": "260",
                        "block_control_point": {"x": 7, "y": 3},
                        "block_position": [
                            {"x": 7, "y": 4},
                            {"x": 7, "y": 2},
                            {"x": 6, "y": 3},
                            {"x": 8, "y": 3},
                            {"x": 7, "y": 3},
                        ],
                    },
                    {
                        "block_type": "도적",
                        "block_class": "섀도어",
                        "block_level": "200",
                        "block_control_point": {"x": -11, "y": -5},
                        "block_position": [
                            {"x": -10, "y": -4},
                            {"x": -11, "y": -6},
                            {"x": -11, "y": -4},
                            {"x": -11, "y": -5},
                        ],
                    },
                    {
                        "block_type": "도적",
                        "block_class": "듀얼블레이더",
                        "block_level": "200",
                        "block_control_point": {"x": -10, "y": -7},
                        "block_position": [
                            {"x": -9, "y": -8},
                            {"x": -10, "y": -6},
                            {"x": -10, "y": -8},
                            {"x": -10, "y": -7},
                        ],
                    },
                    {
                        "block_type": "도적",
                        "block_class": "칼리",
                        "block_level": "222",
                        "block_control_point": {"x": 0, "y": 0},
                        "block_position": [
                            {"x": -1, "y": -1},
                            {"x": 1, "y": 0},
                            {"x": -1, "y": 0},
                            {"x": 0, "y": 0},
                        ],
                    },
                    {
                        "block_type": "해적",
                        "block_class": "엔젤릭버스터",
                        "block_level": "260",
                        "block_control_point": {"x": -10, "y": 0},
                        "block_position": [
                            {"x": -8, "y": 1},
                            {"x": -9, "y": 1},
                            {"x": -11, "y": 0},
                            {"x": -10, "y": 1},
                            {"x": -10, "y": 0},
                        ],
                    },
                    {
                        "block_type": "해적",
                        "block_class": "메카닉",
                        "block_level": "250",
                        "block_control_point": {"x": -9, "y": -5},
                        "block_position": [
                            {"x": -7, "y": -6},
                            {"x": -8, "y": -6},
                            {"x": -10, "y": -5},
                            {"x": -9, "y": -6},
                            {"x": -9, "y": -5},
                        ],
                    },
                    {
                        "block_type": "해적",
                        "block_class": "아크",
                        "block_level": "200",
                        "block_control_point": {"x": -10, "y": 4},
                        "block_position": [
                            {"x": -11, "y": 5},
                            {"x": -9, "y": 4},
                            {"x": -10, "y": 5},
                            {"x": -10, "y": 4},
                        ],
                    },
                    {
                        "block_type": "궁수",
                        "block_class": "윈드브레이커",
                        "block_level": "250",
                        "block_control_point": {"x": 6, "y": 0},
                        "block_position": [
                            {"x": 6, "y": -2},
                            {"x": 6, "y": 2},
                            {"x": 6, "y": -1},
                            {"x": 6, "y": 1},
                            {"x": 6, "y": 0},
                        ],
                    },
                    {
                        "block_type": "도적",
                        "block_class": "나이트워커",
                        "block_level": "200",
                        "block_control_point": {"x": -11, "y": 7},
                        "block_position": [
                            {"x": -10, "y": 6},
                            {"x": -11, "y": 8},
                            {"x": -11, "y": 6},
                            {"x": -11, "y": 7},
                        ],
                    },
                    {
                        "block_type": "해적",
                        "block_class": "스트라이커",
                        "block_level": "201",
                        "block_control_point": {"x": -3, "y": -6},
                        "block_position": [
                            {"x": -2, "y": -5},
                            {"x": -4, "y": -6},
                            {"x": -3, "y": -5},
                            {"x": -3, "y": -6},
                        ],
                    },
                    {
                        "block_type": "해적",
                        "block_class": "바이퍼",
                        "block_level": "210",
                        "block_control_point": {"x": -5, "y": -5},
                        "block_position": [
                            {"x": -6, "y": -6},
                            {"x": -4, "y": -5},
                            {"x": -5, "y": -6},
                            {"x": -5, "y": -5},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "비숍",
                        "block_level": "228",
                        "block_control_point": {"x": 8, "y": -1},
                        "block_position": [
                            {"x": 8, "y": -2},
                            {"x": 7, "y": -1},
                            {"x": 9, "y": -1},
                            {"x": 8, "y": -1},
                        ],
                    },
                    {
                        "block_type": "전사",
                        "block_class": "팔라딘",
                        "block_level": "200",
                        "block_control_point": {"x": -8, "y": -2},
                        "block_position": [
                            {"x": -7, "y": -3},
                            {"x": -8, "y": -3},
                            {"x": -7, "y": -2},
                            {"x": -8, "y": -2},
                        ],
                    },
                    {
                        "block_type": "궁수",
                        "block_class": "패스파인더",
                        "block_level": "200",
                        "block_control_point": {"x": -8, "y": -9},
                        "block_position": [
                            {"x": -6, "y": -9},
                            {"x": -9, "y": -9},
                            {"x": -7, "y": -9},
                            {"x": -8, "y": -9},
                        ],
                    },
                    {
                        "block_type": "도적",
                        "block_class": "호영",
                        "block_level": "200",
                        "block_control_point": {"x": -4, "y": -9},
                        "block_position": [
                            {"x": -5, "y": -8},
                            {"x": -3, "y": -9},
                            {"x": -5, "y": -9},
                            {"x": -4, "y": -9},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "플레임위자드",
                        "block_level": "200",
                        "block_control_point": {"x": -7, "y": -5},
                        "block_position": [
                            {"x": -7, "y": -4},
                            {"x": -8, "y": -5},
                            {"x": -6, "y": -5},
                            {"x": -7, "y": -5},
                        ],
                    },
                    {
                        "block_type": "하이브리드",
                        "block_class": "제논",
                        "block_level": "200",
                        "block_control_point": {"x": -7, "y": 5},
                        "block_position": [
                            {"x": -8, "y": 4},
                            {"x": -7, "y": 6},
                            {"x": -7, "y": 4},
                            {"x": -7, "y": 5},
                        ],
                    },
                    {
                        "block_type": "도적",
                        "block_class": "나이트로드",
                        "block_level": "200",
                        "block_control_point": {"x": -11, "y": -8},
                        "block_position": [
                            {"x": -10, "y": -9},
                            {"x": -11, "y": -7},
                            {"x": -11, "y": -9},
                            {"x": -11, "y": -8},
                        ],
                    },
                    {
                        "block_type": "도적",
                        "block_class": "팬텀",
                        "block_level": "200",
                        "block_control_point": {"x": -8, "y": 6},
                        "block_position": [
                            {"x": -9, "y": 5},
                            {"x": -8, "y": 7},
                            {"x": -8, "y": 5},
                            {"x": -8, "y": 6},
                        ],
                    },
                    {
                        "block_type": "전사",
                        "block_class": "데몬슬레이어",
                        "block_level": "200",
                        "block_control_point": {"x": -2, "y": -6},
                        "block_position": [
                            {"x": -1, "y": -7},
                            {"x": -2, "y": -7},
                            {"x": -1, "y": -6},
                            {"x": -2, "y": -6},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "일리움",
                        "block_level": "200",
                        "block_control_point": {"x": 7, "y": -3},
                        "block_position": [
                            {"x": 8, "y": -3},
                            {"x": 7, "y": -4},
                            {"x": 7, "y": -2},
                            {"x": 7, "y": -3},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "루미너스",
                        "block_level": "200",
                        "block_control_point": {"x": -9, "y": 7},
                        "block_position": [
                            {"x": -10, "y": 7},
                            {"x": -9, "y": 8},
                            {"x": -9, "y": 6},
                            {"x": -9, "y": 7},
                        ],
                    },
                    {
                        "block_type": "전사",
                        "block_class": "데몬어벤져",
                        "block_level": "200",
                        "block_control_point": {"x": -4, "y": -7},
                        "block_position": [
                            {"x": -3, "y": -8},
                            {"x": -4, "y": -8},
                            {"x": -3, "y": -7},
                            {"x": -4, "y": -7},
                        ],
                    },
                    {
                        "block_type": "궁수",
                        "block_class": "와일드헌터",
                        "block_level": "203",
                        "block_control_point": {"x": 8, "y": 0},
                        "block_position": [
                            {"x": 10, "y": 0},
                            {"x": 7, "y": 0},
                            {"x": 9, "y": 0},
                            {"x": 8, "y": 0},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "아크메이지(썬,콜)",
                        "block_level": "280",
                        "block_control_point": {"x": -9, "y": -1},
                        "block_position": [
                            {"x": -9, "y": 0},
                            {"x": -9, "y": -2},
                            {"x": -10, "y": -1},
                            {"x": -8, "y": -1},
                            {"x": -9, "y": -1},
                        ],
                    },
                    {
                        "block_type": "메이플 M 캐릭터",
                        "block_class": "모바일 캐릭터",
                        "block_level": "170",
                        "block_control_point": {"x": -11, "y": 2},
                        "block_position": [
                            {"x": -11, "y": 4},
                            {"x": -11, "y": 1},
                            {"x": -11, "y": 3},
                            {"x": -11, "y": 2},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "배틀메이지",
                        "block_level": "200",
                        "block_control_point": {"x": 8, "y": 1},
                        "block_position": [
                            {"x": 8, "y": 2},
                            {"x": 9, "y": 1},
                            {"x": 7, "y": 1},
                            {"x": 8, "y": 1},
                        ],
                    },
                    {
                        "block_type": "전사",
                        "block_class": "제로",
                        "block_level": "200",
                        "block_control_point": {"x": -8, "y": 3},
                        "block_position": [
                            {"x": -7, "y": 2},
                            {"x": -8, "y": 2},
                            {"x": -7, "y": 3},
                            {"x": -8, "y": 3},
                        ],
                    },
                    {
                        "block_type": "전사",
                        "block_class": "블래스터",
                        "block_level": "200",
                        "block_control_point": {"x": -10, "y": 3},
                        "block_position": [
                            {"x": -9, "y": 2},
                            {"x": -10, "y": 2},
                            {"x": -9, "y": 3},
                            {"x": -10, "y": 3},
                        ],
                    },
                    {
                        "block_type": "궁수",
                        "block_class": "신궁",
                        "block_level": "200",
                        "block_control_point": {"x": -1, "y": -4},
                        "block_position": [
                            {"x": -1, "y": -2},
                            {"x": -1, "y": -5},
                            {"x": -1, "y": -3},
                            {"x": -1, "y": -4},
                        ],
                    },
                    {
                        "block_type": "해적",
                        "block_class": "은월",
                        "block_level": "210",
                        "block_control_point": {"x": -10, "y": 9},
                        "block_position": [
                            {"x": -11, "y": 10},
                            {"x": -10, "y": 8},
                            {"x": -11, "y": 9},
                            {"x": -10, "y": 9},
                        ],
                    },
                    {
                        "block_type": "해적",
                        "block_class": "메카닉",
                        "block_level": "200",
                        "block_control_point": {"x": -8, "y": -8},
                        "block_position": [
                            {"x": -9, "y": -7},
                            {"x": -7, "y": -8},
                            {"x": -8, "y": -7},
                            {"x": -8, "y": -8},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "키네시스",
                        "block_level": "200",
                        "block_control_point": {"x": -6, "y": -7},
                        "block_position": [
                            {"x": -6, "y": -8},
                            {"x": -7, "y": -7},
                            {"x": -5, "y": -7},
                            {"x": -6, "y": -7},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "에반",
                        "block_level": "200",
                        "block_control_point": {"x": 9, "y": -4},
                        "block_position": [
                            {"x": 9, "y": -3},
                            {"x": 8, "y": -4},
                            {"x": 10, "y": -4},
                            {"x": 9, "y": -4},
                        ],
                    },
                    {
                        "block_type": "궁수",
                        "block_class": "메르세데스",
                        "block_level": "200",
                        "block_control_point": {"x": 3, "y": 0},
                        "block_position": [
                            {"x": 5, "y": 0},
                            {"x": 2, "y": 0},
                            {"x": 4, "y": 0},
                            {"x": 3, "y": 0},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "아크메이지(불,독)",
                        "block_level": "250",
                        "block_control_point": {"x": 10, "y": -2},
                        "block_position": [
                            {"x": 11, "y": -2},
                            {"x": 9, "y": -2},
                            {"x": 10, "y": -3},
                            {"x": 10, "y": -1},
                            {"x": 10, "y": -2},
                        ],
                    },
                    {
                        "block_type": "마법사",
                        "block_class": "라라",
                        "block_level": "224",
                        "block_control_point": {"x": -7, "y": 0},
                        "block_position": [
                            {"x": -8, "y": 0},
                            {"x": -7, "y": -1},
                            {"x": -7, "y": 1},
                            {"x": -7, "y": 0},
                        ],
                    },
                    {
                        "block_type": "전사",
                        "block_class": "아델",
                        "block_level": "204",
                        "block_control_point": {"x": -2, "y": -8},
                        "block_position": [
                            {"x": -1, "y": -9},
                            {"x": -2, "y": -9},
                            {"x": -1, "y": -8},
                            {"x": -2, "y": -8},
                        ],
                    },
                ],
                "union_inner_stat": [
                    {"stat_field_id": "0", "stat_field_effect": "유니온 STR"},
                    {"stat_field_id": "1", "stat_field_effect": "유니온 DEX"},
                    {"stat_field_id": "2", "stat_field_effect": "유니온 최대 HP"},
                    {"stat_field_id": "3", "stat_field_effect": "유니온 마력"},
                    {"stat_field_id": "4", "stat_field_effect": "유니온 LUK"},
                    {"stat_field_id": "5", "stat_field_effect": "유니온 INT"},
                    {"stat_field_id": "6", "stat_field_effect": "유니온 공격력"},
                    {"stat_field_id": "7", "stat_field_effect": "유니온 최대 MP"},
                ],
            },
            request=httpx.Request(
                "GET",
                "https://open.api.nexon.com/maplestory/v1/user/union-raider",
                params=params,
                headers=headers,
            ),
        )
    elif "/user/union-artifact" in url:
        return httpx.Response(
            200,
            json={
                "date": "2024-02-21T00:00+09:00",
                "union_artifact_effect": [
                    {"name": "올스탯 150 증가", "level": 10},
                    {"name": "공격력 18, 마력 18 증가", "level": 6},
                    {"name": "데미지 15.00% 증가", "level": 10},
                    {"name": "보스 몬스터 공격 시 데미지 15.00% 증가", "level": 10},
                    {"name": "몬스터 방어율 무시 20% 증가", "level": 10},
                    {"name": "버프 지속시간 20% 증가", "level": 10},
                    {"name": "아이템 드롭률 7% 증가", "level": 6},
                    {"name": "크리티컬 확률 20% 증가", "level": 10},
                    {"name": "크리티컬 데미지 2.40% 증가", "level": 6},
                ],
                "union_artifact_crystal": [
                    {
                        "name": "크리스탈 : 주황버섯",
                        "validity_flag": "0",
                        "date_expire": "2024-03-21T20:21+09:00",
                        "level": 5,
                        "crystal_option_name_1": "버프 지속시간 증가",
                        "crystal_option_name_2": "보스 몬스터 공격 시 데미지 증가",
                        "crystal_option_name_3": "몬스터 방어율 무시 증가",
                    },
                    {
                        "name": "크리스탈 : 슬라임",
                        "validity_flag": "0",
                        "date_expire": "2024-03-21T20:21+09:00",
                        "level": 5,
                        "crystal_option_name_1": "버프 지속시간 증가",
                        "crystal_option_name_2": "보스 몬스터 공격 시 데미지 증가",
                        "crystal_option_name_3": "몬스터 방어율 무시 증가",
                    },
                    {
                        "name": "크리스탈 : 뿔버섯",
                        "validity_flag": "0",
                        "date_expire": "2024-03-21T20:21+09:00",
                        "level": 5,
                        "crystal_option_name_1": "올스탯 증가",
                        "crystal_option_name_2": "데미지 증가",
                        "crystal_option_name_3": "크리티컬 확률 증가",
                    },
                    {
                        "name": "크리스탈 : 스텀프",
                        "validity_flag": "0",
                        "date_expire": "2024-03-21T20:21+09:00",
                        "level": 5,
                        "crystal_option_name_1": "올스탯 증가",
                        "crystal_option_name_2": "데미지 증가",
                        "crystal_option_name_3": "크리티컬 확률 증가",
                    },
                    {
                        "name": "크리스탈 : 스톤골렘",
                        "validity_flag": "0",
                        "date_expire": "2024-03-21T20:21+09:00",
                        "level": 4,
                        "crystal_option_name_1": "크리티컬 데미지 증가",
                        "crystal_option_name_2": "공격력/마력 증가",
                        "crystal_option_name_3": "아이템 드롭률 증가",
                    },
                    {
                        "name": "크리스탈 : 발록",
                        "validity_flag": "0",
                        "date_expire": "2024-03-21T20:21+09:00",
                        "level": 2,
                        "crystal_option_name_1": "크리티컬 데미지 증가",
                        "crystal_option_name_2": "아이템 드롭률 증가",
                        "crystal_option_name_3": "공격력/마력 증가",
                    },
                ],
                "union_artifact_remain_ap": 4,
            },
            request=httpx.Request(
                "GET",
                "https://open.api.nexon.com/maplestory/v1/user/union-artifact",
                params=params,
                headers=headers,
            ),
        )
    elif "/user/union" in url:
        return httpx.Response(
            200,
            json={
                "date": "2024-02-21T00:00+09:00",
                "union_level": 8871,
                "union_grade": "그랜드 마스터 유니온 2",
                "union_artifact_level": 35,
                "union_artifact_exp": 2956,
                "union_artifact_point": 8000,
                "artifact_level": 35,
                "artifact_exp": 2956,
                "artifact_point": 8000,
            },
            request=httpx.Request(
                "GET",
                "https://open.api.nexon.com/maplestory/v1/user/union",
                params=params,
                headers=headers,
            ),
        )
    else:
        return httpx.Response(
            404,
            request=httpx.Request("GET", url, params=params, headers=headers),
        )


class TestUnion:
    # Guild object has computed fields for level, point, fame, member_count, member_names, master_name, skills, noblesse_skills, mark, and is_custom_mark.
    def test_computed_fields(self, mocker):
        mocker.patch("httpx.get", side_effect=custom_side_effect)

        # Create a Guild object
        union = Union(character_name="온앤온")

        # Test the computed fields
        assert union.union_info == get_union_info("온앤온")
        assert union.date == yesterday()
        assert union.level == 8871
        assert union.grade == "그랜드 마스터 유니온 2"
        assert union.raider_info == get_union_raider_info("온앤온")
        assert union.raider_stats == UnionStats(
            [
                UnionStat(stat="DEX 320 증가"),
                UnionStat(stat="INT 660 증가"),
                UnionStat(stat="LUK 440 증가"),
                UnionStat(stat="STR 440 증가"),
                UnionStat(stat="경험치 획득량 10% 증가"),
                UnionStat(stat="공격 시 20%의 확률로 데미지 16% 증가"),
                UnionStat(stat="공격력 20 증가"),
                UnionStat(stat="마력 20 증가"),
                UnionStat(stat="메소 획득량 4% 증가"),
                UnionStat(stat="방어율 무시 5% 증가"),
                UnionStat(stat="버프 지속시간 20% 증가"),
                UnionStat(stat="보스 몬스터 공격 시 데미지 5% 증가"),
                UnionStat(stat="상태 이상 내성 4 증가"),
                UnionStat(stat="스킬 재사용 대기시간 5% 감소"),
                UnionStat(stat="적 공격마다 70%의 확률로 순수 MP의 8% 회복"),
                UnionStat(stat="최대 MP 6% 증가"),
                UnionStat(stat="크리티컬 데미지 5% 증가"),
                UnionStat(stat="크리티컬 확률 8% 증가"),
            ]
        )

        assert union.공격대원효과 == UnionStats(
            [
                UnionStat(stat="DEX 320 증가"),
                UnionStat(stat="INT 660 증가"),
                UnionStat(stat="LUK 440 증가"),
                UnionStat(stat="STR 440 증가"),
                UnionStat(stat="경험치 획득량 10% 증가"),
                UnionStat(stat="공격 시 20%의 확률로 데미지 16% 증가"),
                UnionStat(stat="공격력 20 증가"),
                UnionStat(stat="마력 20 증가"),
                UnionStat(stat="메소 획득량 4% 증가"),
                UnionStat(stat="방어율 무시 5% 증가"),
                UnionStat(stat="버프 지속시간 20% 증가"),
                UnionStat(stat="보스 몬스터 공격 시 데미지 5% 증가"),
                UnionStat(stat="상태 이상 내성 4 증가"),
                UnionStat(stat="스킬 재사용 대기시간 5% 감소"),
                UnionStat(stat="적 공격마다 70%의 확률로 순수 MP의 8% 회복"),
                UnionStat(stat="최대 MP 6% 증가"),
                UnionStat(stat="크리티컬 데미지 5% 증가"),
                UnionStat(stat="크리티컬 확률 8% 증가"),
            ]
        )
        assert (
            union.occupied_stats
            == union.공격대점령효과
            == UnionStats(
                [
                    UnionStat(stat="INT 25 증가"),
                    UnionStat(stat="LUK 5 증가"),
                    UnionStat(stat="마력 5 증가"),
                    UnionStat(stat="방어율 무시 33% 증가"),
                    UnionStat(stat="버프 지속시간 40% 증가"),
                    UnionStat(stat="보스 몬스터 공격 시 데미지 23% 증가"),
                    UnionStat(stat="크리티컬 데미지 20.00% 증가"),
                    UnionStat(stat="크리티컬 확률 11% 증가"),
                ]
            )
        )
        assert isinstance(union.artifact, UnionArtifact)
        assert isinstance(union.artifact.effects, list)
        assert isinstance(union.artifact.effects[0], UnionArtifactEffect)
        assert union.artifact.effects[0] == UnionArtifactEffect(
            name="올스탯 150 증가", level=10
        )
        assert isinstance(union.artifact.crystals, list)

        first_crystal = union.artifact.crystals[0]
        assert isinstance(first_crystal, UnionArtifactCrystal)
        assert first_crystal.name == "크리스탈 : 주황버섯"
        assert first_crystal.date_expire == datetime(2024, 3, 21, 20, 21, tzinfo=KST_TZ)
        assert first_crystal.level == 5
        assert first_crystal.expired is False
        assert first_crystal.options == [
            "버프 지속시간 증가",
            "보스 몬스터 공격 시 데미지 증가",
            "몬스터 방어율 무시 증가",
        ]

        assert union.artifact.remain_ap == 4
        assert (
            union.artifact_effects
            == union.아티팩트효과
            == [
                UnionArtifactEffect(name="올스탯 150 증가", level=10),
                UnionArtifactEffect(name="공격력 18, 마력 18 증가", level=6),
                UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
                UnionArtifactEffect(
                    name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
                ),
                UnionArtifactEffect(name="몬스터 방어율 무시 20% 증가", level=10),
                UnionArtifactEffect(name="버프 지속시간 20% 증가", level=10),
                UnionArtifactEffect(name="아이템 드롭률 7% 증가", level=6),
                UnionArtifactEffect(name="크리티컬 확률 20% 증가", level=10),
                UnionArtifactEffect(name="크리티컬 데미지 2.40% 증가", level=6),
            ]
        )

    # Union instance has a 'grade' property that returns the grade of the character's union.
    def test_union_grade_property(self, mocker):
        # Mock the get_union_info function
        mocker.patch("httpx.get", side_effect=custom_side_effect)

        # Create a Union instance
        union = Union(character_name="CharacterName", date=datetime(2024, 3, 1))

        # Assert the grade property returns the correct value
        assert union.grade == "그랜드 마스터 유니온 2"

    # Union instance has a 'level' property that returns the level of the character's union.
    def test_union_level_property(self, mocker):
        # Mock the get_union_info function
        mocker.patch("httpx.get", side_effect=custom_side_effect)

        # Create a Union instance
        union = Union(character_name="CharacterName", date=datetime(2024, 3, 1))

        # Assert the level property returns the correct value
        assert union.level == 8871

    # Union instance has a 'raider_stats' property that returns a summary of the stats of the character's union raiders.
    def test_raider_stats_property(self, mocker):
        # Mock the get_union_raider_info function
        mocker.patch(
            "maplestory.services.union.get_union_raider_info",
            return_value=UnionRaider(
                date=datetime(2024, 3, 1),
                union_raider_stat=[
                    "STR 80 증가",
                    "STR 80 증가",
                    "STR 80 증가",
                    "크리티컬 데미지 5% 증가",
                    "크리티컬 확률 4% 증가",
                    "크리티컬 확률 4% 증가",
                    "STR, DEX, LUK 40 증가",
                    "공격력/마력 20 증가",
                ],
                union_occupied_stat=["버프 지속시간 40% 증가", "방어율 무시 33% 증가"],
                union_inner_stat=[],
                union_block=[],
            ),
        )

        # Create a Union instance
        union = Union(character_name="CharacterName", date=datetime(2024, 3, 1))

        # Assert the raider_stats property returns the expected value
        assert union.raider_stats == UnionStats(
            root=[
                UnionStat(stat="DEX 40 증가"),
                UnionStat(stat="LUK 40 증가"),
                UnionStat(stat="STR 280 증가"),
                UnionStat(stat="공격력 20 증가"),
                UnionStat(stat="마력 20 증가"),
                UnionStat(stat="크리티컬 데미지 5% 증가"),
                UnionStat(stat="크리티컬 확률 8% 증가"),
            ]
        )

    # Union instance has an 'occupied_stats' property that returns a summary of the stats of the character's union occupation.
    def test_occupied_stats_property(self, mocker):
        # Mock the get_union_raider_info function
        mocker.patch(
            "maplestory.services.union.get_union_raider_info",
            return_value=UnionRaider(
                date=datetime(2022, 1, 1),
                union_raider_stat=[
                    "스킬 재사용 대기시간 5% 감소",
                    "STR 80 증가",
                    "공격력/마력 20 증가",
                ],
                union_occupied_stat=[
                    "크리티컬 데미지 20.00% 증가",
                    "보스 몬스터 공격 시 데미지 23% 증가",
                    "방어율 무시 33% 증가",
                ],
                union_inner_stat=[],
                union_block=[],
            ),
        )

        # Create a Union instance
        union = Union(character_name="CharacterName", date=datetime(2024, 3, 1))

        # Assert that the occupied_stats property returns the expected UnionStats object
        assert isinstance(union.occupied_stats, UnionStats)
        assert union.occupied_stats.group_stats() == {
            ("방어율 무시", True): [UnionStat(stat="방어율 무시 33% 증가")],
            ("보스 몬스터 공격 시 데미지", True): [
                UnionStat(stat="보스 몬스터 공격 시 데미지 23% 증가")
            ],
            ("크리티컬 데미지", True): [UnionStat(stat="크리티컬 데미지 20.00% 증가")],
        }
        assert union.occupied_stats.group_with_split_multiple() == {
            ("방어율 무시", True): [UnionStat(stat="방어율 무시 33% 증가")],
            ("보스 몬스터 공격 시 데미지", True): [
                UnionStat(stat="보스 몬스터 공격 시 데미지 23% 증가")
            ],
            ("크리티컬 데미지", True): [UnionStat(stat="크리티컬 데미지 20.00% 증가")],
        }

    # Union instance has an 'artifact_effects' property that returns a list of the character's union artifact effects.
    def test_union_artifact_effects_property(self, mocker):
        mocker.patch("httpx.get", side_effect=custom_side_effect)

        # Create a Union instance
        union = Union(character_name="CharacterName", date=datetime(2024, 3, 1))

        assert union.artifact_effects == [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="공격력 18, 마력 18 증가", level=6),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
            UnionArtifactEffect(name="몬스터 방어율 무시 20% 증가", level=10),
            UnionArtifactEffect(name="버프 지속시간 20% 증가", level=10),
            UnionArtifactEffect(name="아이템 드롭률 7% 증가", level=6),
            UnionArtifactEffect(name="크리티컬 확률 20% 증가", level=10),
            UnionArtifactEffect(name="크리티컬 데미지 2.40% 증가", level=6),
        ]


class TestUnionStat:
    # can parse a valid stat string into its components
    def test_parse_valid_stat_string(self):
        # Initialize the UnionStat class with a valid stat string
        stat = UnionStat(stat="공격력 20 증가")

        # Assert that the parsed properties are correct
        assert stat.name == "공격력"
        assert stat.is_percent is False
        assert stat.value == 20
        assert stat.updown == "증가"

        # Assert that the parsed_stat property is correct
        assert stat.parsed_stat == {
            "name": "공격력",
            "value": "20",
            "percent": "",
            "updown": "증가",
        }

    # can handle a stat with a missing percent sign
    def test_handle_missing_percent_sign(self):
        # Initialize the UnionStat class with a stat string missing the percent sign
        stat = UnionStat(stat="공격력 20 증가")

        # Assert that the is_percent property is False
        assert stat.is_percent is False

    # can correctly identify the name of the stat
    def test_identify_stat_name(self):
        # Initialize the UnionStat class with a valid stat string
        stat = UnionStat(stat="공격력 20 증가")

        # Assert that the name property is correct
        assert stat.name == "공격력"

    # can add two non-percentage stats
    def test_add_two_non_percentage_stats(self):
        # Initialize the UnionStat class with two non-percentage stats
        stat1 = UnionStat(stat="공격력 20 증가")
        stat2 = UnionStat(stat="마력 30 증가")

        # Add the two stats together
        with pytest.raises(ValueError, match="Cannot add different stats."):
            _ = stat1 + stat2

    # can add two stats with the same name and updown
    def test_add_stats_with_same_name_and_updown(self):
        # Initialize two UnionStat instances with the same name and updown
        stat1 = UnionStat(stat="공격력 20 증가")
        stat2 = UnionStat(stat="공격력 30 증가")

        # Add the two stats together
        result = stat1 + stat2

        # Assert that the result is a UnionStat instance
        assert isinstance(result, UnionStat)

        # Assert that the result has the correct name, value, and updown
        assert result.name == "공격력"
        assert result.value == 50
        assert result.updown == "증가"

    # can correctly identify whether the stat is a percentage or not
    def test_stat_percentage_identification(self):
        # Initialize the UnionStat class with a stat string that is a percentage
        stat1 = UnionStat(stat="크리티컬 데미지 20% 증가")

        # Assert that the is_percent property is True
        assert stat1.is_percent is True

        # Initialize the UnionStat class with a stat string that is not a percentage
        stat2 = UnionStat(stat="공격력 20 증가")

        # Assert that the is_percent property is False
        assert stat2.is_percent is False

    # can correctly identify the updown of the stat
    def test_identify_updown_of_stat(self):
        # Initialize the UnionStat class with a valid stat string
        stat1 = UnionStat(stat="공격력 20 증가")
        stat2 = UnionStat(stat="마력 10 감소")

        # Assert that the updown property is correct
        assert stat1.updown == "증가"
        assert stat2.updown == "감소"

    # can add two percentage stats
    def test_add_two_percentage_stats(self):
        # Initialize the UnionStat class with two percentage stats
        stat1 = UnionStat(stat="공격력 20% 증가")
        stat2 = UnionStat(stat="마력 30% 증가")

        # Add the two stats together
        with pytest.raises(ValueError, match="Cannot add different stats."):
            _ = stat1 + stat2

    # can correctly identify a multi-name stat
    def test_correctly_identify_multi_name_stat(self):
        # Initialize the UnionStat class with a multi-name stat string
        stat = UnionStat(stat="STR, DEX, LUK 40 증가")

        # Assert that the parsed properties are correct
        assert stat.name == "STR, DEX, LUK"
        assert stat.is_percent is False
        assert stat.value == 40
        assert stat.updown == "증가"

        # Assert that the parsed_stat property is correct
        assert stat.parsed_stat == {
            "name": "STR, DEX, LUK",
            "value": "40",
            "percent": "",
            "updown": "증가",
        }

    # can correctly identify the value of the stat
    def test_correctly_identify_value_of_stat(self):
        # Initialize the UnionStat class with a valid stat string
        stat = UnionStat(stat="공격력 20 증가")

        # Assert that the parsed properties are correct
        assert stat.name == "공격력"
        assert stat.is_percent is False
        assert stat.value == 20
        assert stat.updown == "증가"

        # Assert that the parsed_stat property is correct
        assert stat.parsed_stat == {
            "name": "공격력",
            "value": "20",
            "percent": "",
            "updown": "증가",
        }

    # can correctly split a multi-name stat into individual stats
    def test_split_multi_name_stat(self):
        # Initialize the UnionStat class with a multi-name stat string
        stat = UnionStat(stat="STR, DEX, LUK 40 증가")

        # Assert that the parsed properties are correct
        assert stat.name == "STR, DEX, LUK"
        assert stat.is_percent is False
        assert stat.value == 40
        assert stat.updown == "증가"

        # Assert that the parsed_stat property is correct
        assert stat.parsed_stat == {
            "name": "STR, DEX, LUK",
            "value": "40",
            "percent": "",
            "updown": "증가",
        }

        # Assert that the is_multi_name property is True
        assert stat.is_multi_name is True

        # Assert that the multi_name property is correct
        assert stat.multi_name == ["STR", "DEX", "LUK"]
