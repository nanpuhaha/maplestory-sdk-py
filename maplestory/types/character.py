from typing import Annotated, Literal, get_args

from annotated_types import Ge, Le

AbilityNumber = Annotated[int, Ge(1), Le(3)]
CharacterLevel = Annotated[int, Ge(1), Le(300)]
CharacterClassLevel = Literal["0", "1", "2", "3", "4", "5", "6"]
CharacterGender = Literal["남", "여"]
AndroidGender = CharacterGender | None
ItemGender = CharacterGender | None
ItemOptionValue = Annotated[int, Ge(-100)]  # 혼돈의 주문서로 음수 가능
ItemSlotName = Literal[
    "귀고리",
    "기계 심장",
    "눈장식",
    "망토",
    "모자",
    "무기",
    "반지1",
    "반지2",
    "반지3",
    "반지4",
    "뱃지",
    "벨트",
    "보조무기",
    "상의",
    "신발",
    "어깨장식",
    "얼굴장식",
    "엠블렘",
    "장갑",
    "펜던트",
    "펜던트2",
    "포켓 아이템",
    "하의",
    "훈장",
]
LabelName = Literal["스페셜라벨", "레드라벨", "블랙라벨", "마스터라벨"] | None
LinkSkillLevel = Annotated[int, Ge(1), Le(10)]
PetSkill = Literal[
    "버프 스킬 자동 사용",
    "아이템 줍기",
    "이동반경 확대",
    "자동 줍기",
    "펫 자이언트 스킬",
    "펫 훈련 스킬",
    "HP 물약충전",
    "MP 물약충전",
]
HyperStatLevel = Annotated[int, Ge(0), Le(15)]
HyperStatType = Literal[
    "STR",
    "DEX",
    "INT",
    "LUK",
    "HP",
    "MP",
    "DF/TF/PP",
    "크리티컬 확률",
    "크리티컬 데미지",
    "방어율 무시",
    "데미지",
    "보스 몬스터 공격 시 데미지 증가",
    "상태 이상 내성",
    "공격력/마력",
    "획득 경험치",
    "아케인포스",
    "일반 몬스터 공격 시 데미지 증가",
]
VCoreType = Literal["강화코어", "스킬코어", "특수코어"] | None
VCoreLevel = Annotated[int, Ge(1), Le(30)]

SkillGrade = Literal[
    "0", "1", "1.5", "2", "2.5", "3", "4", "5", "6", "hyperpassive", "hyperactive"
]
SkillGradeList = get_args(SkillGrade)

Classes = Literal[
    "초보자",
    "검사",
    "파이터",
    "페이지",
    "스피어맨",
    "크루세이더",
    "나이트",
    "버서커",
    "히어로",
    "팔라딘",
    "다크나이트",
    "매지션",
    "위자드(불,독)",
    "위자드(썬,콜)",
    "클레릭",
    "메이지(불,독)",
    "메이지(썬,콜)",
    "프리스트",
    "아크메이지(불,독)",
    "아크메이지(썬,콜)",
    "비숍",
    "아처",
    "헌터",
    "사수",
    "레인저",
    "저격수",
    "보우마스터",
    "신궁",
    "패스파인더",
    "에인션트아처",
    "에인션트 아처",
    "체이서",
    "패스파인더",
    "로그",
    "어쌔신",
    "시프",
    "허밋",
    "시프마스터",
    "나이트로드",
    "섀도어",
    "세미듀어러",
    "듀어러",
    "듀얼마스터",
    "슬래셔",
    "듀얼블레이더",
    "해적",
    "인파이터",
    "건슬링거",
    "캐논슈터",
    "버커니어",
    "발키리",
    "캐논블래스터",
    "바이퍼",
    "캡틴",
    "캐논마스터",
    "노블레스",
    "소울마스터",
    "플레임위자드",
    "윈드브레이커",
    "나이트워커",
    "스트라이커",
    "미하일",
    "시티즌",
    "배틀메이지",
    "와일드헌터",
    "메카닉",
    "제논",
    "블래스터",
    "데몬슬레이어",
    "데몬어벤져",
    "아란",
    "에반",
    "루미너스",
    "메르세데스",
    "팬텀",
    "은월",
    "카이저",
    "카인",
    "카데나",
    "엔젤릭버스터",
    "아델",
    "일리움",
    "칼리",
    "아크",
    "라라",
    "호영",
    "제로",
    "키네시스",
]


def is_valid_class(class_name: str) -> bool:
    allowed_job_types = get_args(Classes)
    return class_name in allowed_job_types
