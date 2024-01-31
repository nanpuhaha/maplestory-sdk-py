from typing import Literal

ArtifactCrystalOption = Literal[
    "공격력/마력 증가",
    "데미지 증가",
    "몬스터 방어율 무시 증가",
    "버프 지속시간 증가",
    "보스 몬스터 공격 시 데미지 증가",
    "아이템 드롭률 증가",
    "올스탯 증가",
    "재사용 대기시간 미적용 확률 증가",
    "최대 HP/MP 증가",
    "추가 경험치 획득 증가",
    "크리티컬 데미지 증가",
    "크리티컬 확률 증가",
]

UnionWorldName = Literal[
    "스카니아",
    "베라",
    "루나",
    "제니스",
    "크로아",
    "유니온",
    "엘리시움",
    "이노시스",
    "레드",
    "오로라",
    "아케인",
    "노바",
    "리부트",
    "리부트2",
]

UnionRaiderStatName = Literal[
    "공격력/마력",
    "데미지 증가",
    "몬스터 방어율 무시 증가",
    "버프 지속시간 증가",
    "보스 몬스터 공격 시 데미지 증가",
    "아이템 드롭률 증가",
    "올스탯 증가",
    "스킬 재사용 대기시간",
    "최대 HP/MP 증가",
    "추가 경험치 획득 증가",
    "크리티컬 데미지 증가",
    "크리티컬 확률 증가",
    "상태 이상 내성",
    "STR",
    "DEX",
    "INT",
    "LUK",
    "STR, DEX, LUK",
    "최대 HP",
]
