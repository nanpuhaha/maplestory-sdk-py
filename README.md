# <p align="center">MapleStory OpenAPI Python Client Library</p>
<p align="center">A simple, but extensible Python implementation for the <a href="https://openapi.nexon.com/game/maplestory/?id=22">MapleStory OpenAPI</a>.</p>
<p align="center">
<a>
    <img src="https://img.shields.io/pypi/pyversions/maplestory" alt="PyPI - Python Version">
</a>
<a>
    <img src="https://img.shields.io/pypi/v/maplestory" alt="PyPI - Version">
</a>
<a href="https://github.com/nanpuhaha/maplestory-py/actions/workflows/pytest.yml">
    <img src="https://github.com/nanpuhaha/maplestory-py/actions/workflows/pytest.yml/badge.svg" alt="Test with pytest">
</a>
<a href="https://codecov.io/gh/nanpuhaha/maplestory-py">
    <img src="https://codecov.io/gh/nanpuhaha/maplestory-py/graph/badge.svg?token=H4S1BWRFJB" alt="codecov">
</a>
</p>

---

> [!NOTE]
> This library can only query data from the **[KMS](https://maplestory.nexon.com)**(Korea MapleStory).

---

## Overview

This library simplifies access to MapleStory's OpenAPI in Python, enabling queries of character, union, guild, and ranking information, as well as checks on Star Force, cubes, and potential abilities.

## Installation

If you are using pip:

```shell
pip install maplestory
```

If you are using poetry:

```shell
poetry add maplestory
```

### Supported Python Versions

Python 3.11 and 3.12 are fully supported and tested. While it may operate on subsequent versions of Python 3, testing against these newer versions is not currently conducted.

### Unsupported Python Versions

- Python < 3.11

### Third Party Libraries and Dependencies

The following libraries will be installed when you install the client library:

- [pydantic v2](https://docs.pydantic.dev)
- [httpx](https://www.python-httpx.org)
- [tenacity](https://tenacity.readthedocs.io)

## Usage

### API credentials

To use the MapleStory OpenAPI, you first need to create a Nexon account at https://www.nexon.com. After creating your account, proceed to the [NEXON OPEN API site](https://openapi.nexon.com) and create a new application. Once your application is created, copy the **API Key** and set it as an environment variable or enter it into a `.env` file within your project.

```conf
# set environment variable
MAPLESTORY_OPENAPI_KEY=INSERT_YOUR_KEY_HERE
```

### Examples

캐릭터명, 길드명 등 이름만 있으면 됩니다.
과거 특정 날짜를 조회하고 싶을 때에는 날짜도 입력하시면 됩니다.
날짜는 기본적으로 어젯자를 기준으로 조회합니다. (추후 API 종류별로 세분화될 예정)

오직 필요한 건 이름 뿐이다.
과거 특정 날짜의 결과를 원하면 날짜도 입력하면 된다.

#### Character

<details>
<summary>Query only the data you want by character name.</summary>

```python
>>> from maplestory.services.character import get_basic_character_info
>>> character_name = "온앤온"
>>> get_basic_character_info(character_name)
CharacterBasic(
    date=datetime.datetime(2024, 2, 3, 0, 0, tzinfo=TzInfo(+09:00)),
    name='온앤온',
    world='스카니아',
    gender='여',
    job='아크메이지(썬,콜)',
    job_level=6,
    level=280,
    exp=25478806855352,
    exp_rate='75.723',
    guild_name='온앤온',
    image='https://open.api.nexon.com/static/maplestory/Character/MBFDMCELMOHJLEJDOKIPBBPFJKDEILAGALCOMHLGJKHBJGGLHCKELOBFDDBONKKPFIHCEONNBGBMNFAALOHOJFEAPIHJHJJNONNDPFPNPIGMNGNIAPADJLGJMKBCPJIANOHOOMLHBJEAKIHALNHFCOLBFIFOCNCEKOHJKMHCGHKFOCBODKAMICEDDJICKHMLEHKKPOEHEEJIJNFMBIGJHOPNDMGLFKOOPJAMJHNKGFNLKDIFNJNFJHIBDDKCPPMF.png'
)
```
</details>

<details>
<summary>Query all character data using just the character name using <code>Character</code> class</summary>

```python
>>> from rich import print
>>> from mapletory.services.character import Character
>>> char = Character(name="온앤온")

>>> print(char)
CharacterBasic(
    date=datetime.datetime(2024, 2, 10, 0, 0, tzinfo=TzInfo(+09:00)),
    name='온앤온',
    world='스카니아',
    gender='여',
    job='아크메이지(썬,콜)',
    job_level=6,
    level=280,
    exp=29014907373569,
    exp_rate=86.232,
    guild_name='온앤온',
    image=<PIL.PngImagePlugin.PngImageFile image mode=RGBA size=96x96 at 0x1063C16D0>
)

>>> print(char.ability)
Ability(
    date=datetime.datetime(2024, 2, 4, 0, 0, tzinfo=TzInfo(+09:00)),
    grade='레전드리',
    info=[
        AbilityInfoItem(grade='레전드리', value='버프 스킬의 지속 시간 50% 증가'),
        AbilityInfoItem(grade='유니크', value='상태 이상에 걸린 대상 공격 시 데미지 8% 증가'),
        AbilityInfoItem(grade='유니크', value='보스 몬스터 공격 시 데미지 10% 증가')
    ],
    remain_fame=465283,
    preset_no=1,
    preset1=AbilityPreset(
        grade='레전드리',
        info=[
            AbilityInfoItem(grade='레전드리', value='버프 스킬의 지속 시간 50% 증가'),
            AbilityInfoItem(grade='유니크', value='상태 이상에 걸린 대상 공격 시 데미지 8% 증가'),
            AbilityInfoItem(grade='유니크', value='보스 몬스터 공격 시 데미지 10% 증가')
        ]
    ),
    preset2=AbilityPreset(
        grade='레전드리',
        info=[
            AbilityInfoItem(grade='레전드리', value='아이템 드롭률 19% 증가'),
            AbilityInfoItem(grade='에픽', value='버프 스킬의 지속 시간 19% 증가'),
            AbilityInfoItem(grade='유니크', value='메소 획득량 15% 증가')
        ]
    ),
    preset3=AbilityPreset(
        grade='에픽',
        info=[
            AbilityInfoItem(grade='에픽', value='모든 능력치 15 증가'),
            AbilityInfoItem(grade='레어', value='모든 능력치 5 증가'),
            AbilityInfoItem(grade='레어', value='모든 능력치 5 증가')
        ]
    )
)
```
</details>

<details>
<summary><h4>Gulid Examples</h4></summary>

```python
>>> from rich import print
>>> from mapletory.services.guild import Guild
>>> guild = Guild(name="리더", world="스카니아")

>>> print(guild)
Guild(
    name='리더',
    world='스카니아',
    id='789b457f357ce6ac3e1bfa1c95ccaac6',
    basic=GuildBasic(
        date=datetime.datetime(2024, 2, 7, 0, 0, tzinfo=TzInfo(+09:00)),
        world='스카니아',
        name='리더',
        level=29,
        fame=65312548,
        point=10000000,
        master_name='아델',
        member_count=160,
        members=[
            '아델',
            '충신정럭이1',
            '충신정럭이2',
            ...
        ],
        skills=[
            GuildSkill(
                name='장사꾼',
                description='[마스터 레벨 : 3]\r\n상점에서 물건을 구매 시 싸게 살 수 있다. 단, 일부 아이템에는 적용되지 않는다.\n[필요 조건]: 길드 10레벨 이상\n[필요 스킬]: 잔돈이 눈에 띄네 3레벨 이상',
                level=3,
                effect='상점에서 물건 구매 시 4% 싸게 구매 가능. 단, 판매 가격 대비 구매 가격이 70% 이상일 경우 적용되지 않음',
                icon=Url('https://open.api.nexon.com/static/maplestory/SkillIcon/KFGDLHOBMI.png')
            ),
            ...
        ],
        noblesse_skills=[
            GuildSkill(
                name='보스 킬링 머신',
                description='[마스터 레벨 : 15]\r\n일정 시간 동안 보스 몬스터 공격 시 데미지가 증가한다.',
                level=15,
                effect='30분 동안 보스 몬스터 공격 시 데미지 30% 증가, 재사용 대기시간 60분',
                icon=Url('https://open.api.nexon.com/static/maplestory/SkillIcon/KFGDLHPBOC.png')
            ),
            ...
        ],
        mark=<PIL.PngImagePlugin.PngImageFile image mode=RGBA size=17x17 at 0x10C9C04D0>,
        is_custom_mark=True
    )
)
```
</details>

<details>
<summary><h4>Union Examples</h4></summary>

공격대원효과, 공격대점령효과, 아티팩트 효과는 각각 **요약된 결과**를 보여줍니다.

예를 들어, `STR 100 증가`가 2개이면 `STR 200 증가`로 표기됩니다.

단, 방어율 무시 옵션는 곱적용되므로 예외적으로 합치지 않습니다. 추후 곱적용 방식으로 계산된 방어율 무시를 제공할 계획입니다.

`STR, DEX, LUK 40 증가`는 `STR 40 증가`, `DEX 40 증가`, `LUK 40 증가`로 분리되며, `공격력/마력 20 증가`는 `공격력 20 증가`, `마력 20 증가`로 분리되어 계산됩니다.

```python
>>> from maplestory.services.union import Union
>>> union = Union(character_name="온앤온")
>>> print(union)
Union(
    character_name='온앤온',
    date=datetime.datetime(2024, 2, 9, 9, 59, 37, 37959, tzinfo=zoneinfo.ZoneInfo(key='Asia/Seoul')),
    level=8870,
    grade='그랜드 마스터 유니온 2',
    raider_stats=UnionStats(
        [
            UnionStat(stat='DEX 320 증가'),
            UnionStat(stat='INT 660 증가'),
            UnionStat(stat='LUK 440 증가'),
            UnionStat(stat='STR 440 증가'),
            UnionStat(stat='경험치 획득량 10% 증가'),
            UnionStat(stat='공격 시 20%의 확률로 데미지 16% 증가'),
            UnionStat(stat='공격력 20 증가'),
            UnionStat(stat='마력 20 증가'),
            UnionStat(stat='메소 획득량 4% 증가'),
            UnionStat(stat='방어율 무시 5% 증가'),
            UnionStat(stat='버프 지속시간 20% 증가'),
            UnionStat(stat='보스 몬스터 공격 시 데미지 5% 증가'),
            UnionStat(stat='상태 이상 내성 4 증가'),
            UnionStat(stat='스킬 재사용 대기시간 5% 감소'),
            UnionStat(stat='적 공격마다 70%의 확률로 순수 MP의 8% 회복'),
            UnionStat(stat='최대 MP 6% 증가'),
            UnionStat(stat='크리티컬 데미지 5% 증가'),
            UnionStat(stat='크리티컬 확률 8% 증가')
        ]
    ),
    occupied_stats=UnionStats(
        [
            UnionStat(stat='INT 25 증가'),
            UnionStat(stat='LUK 5 증가'),
            UnionStat(stat='마력 5 증가'),
            UnionStat(stat='방어율 무시 33% 증가'),
            UnionStat(stat='버프 지속시간 40% 증가'),
            UnionStat(stat='보스 몬스터 공격 시 데미지 23% 증가'),
            UnionStat(stat='크리티컬 데미지 20.00% 증가'),
            UnionStat(stat='크리티컬 확률 11% 증가')
        ]
    ),
    artifact_effects=[
        UnionArtifactEffect(name='올스탯 150 증가', level=10),
        UnionArtifactEffect(name='공격력 18, 마력 18 증가', level=6),
        UnionArtifactEffect(name='데미지 15.00% 증가', level=10),
        UnionArtifactEffect(name='보스 몬스터 공격 시 데미지 15.00% 증가', level=10),
        UnionArtifactEffect(name='몬스터 방어율 무시 20% 증가', level=10),
        UnionArtifactEffect(name='버프 지속시간 20% 증가', level=10),
        UnionArtifactEffect(name='아이템 드롭률 7% 증가', level=6),
        UnionArtifactEffect(name='크리티컬 확률 20% 증가', level=10),
        UnionArtifactEffect(name='크리티컬 데미지 2.40% 증가', level=6)
    ]
)
```
</details>


<details>
<summary><h4>Union - Korean attributes</h4></summary>

You can also use Korean.
- 공격대원효과
- 공격대점령효과
- 아티팩트효과

```python
>>> print(union.공격대원효과)
UnionStats(
    [
        UnionStat('DEX 320 증가'),
        UnionStat('INT 660 증가'),
        UnionStat('LUK 440 증가'),
        UnionStat('STR 440 증가'),
        UnionStat('경험치 획득량 10% 증가'),
        UnionStat('공격 시 20%의 확률로 데미지 16% 증가'),
        UnionStat('공격력 20 증가'),
        UnionStat('마력 20 증가'),
        UnionStat('메소 획득량 4% 증가'),
        UnionStat('방어율 무시 5% 증가'),
        UnionStat('버프 지속시간 20% 증가'),
        UnionStat('보스 몬스터 공격 시 데미지 5% 증가'),
        UnionStat('상태 이상 내성 4 증가'),
        UnionStat('스킬 재사용 대기시간 5% 감소'),
        UnionStat('적 공격마다 70%의 확률로 순수 MP의 8% 회복'),
        UnionStat('최대 MP 6% 증가'),
        UnionStat('크리티컬 데미지 5% 증가'),
        UnionStat('크리티컬 확률 8% 증가')
    ]
)

>>> print(union.공격대점령효과)
UnionStats(
    [
        UnionStat('INT 25 증가'),
        UnionStat('LUK 5 증가'),
        UnionStat('마력 5 증가'),
        UnionStat('방어율 무시 33% 증가'),
        UnionStat('버프 지속시간 40% 증가'),
        UnionStat('보스 몬스터 공격 시 데미지 23% 증가'),
        UnionStat('크리티컬 데미지 20.00% 증가'),
        UnionStat('크리티컬 확률 11% 증가')
    ]
)

>>> print(union.아티팩트효과)
[
    UnionArtifactEffect(name='올스탯 150 증가', level=10),
    UnionArtifactEffect(name='공격력 18, 마력 18 증가', level=6),
    UnionArtifactEffect(name='데미지 15.00% 증가', level=10),
    UnionArtifactEffect(name='보스 몬스터 공격 시 데미지 15.00% 증가', level=10),
    UnionArtifactEffect(name='몬스터 방어율 무시 20% 증가', level=10),
    UnionArtifactEffect(name='버프 지속시간 20% 증가', level=10),
    UnionArtifactEffect(name='아이템 드롭률 7% 증가', level=6),
    UnionArtifactEffect(name='크리티컬 확률 20% 증가', level=10),
    UnionArtifactEffect(name='크리티컬 데미지 2.40% 증가', level=6)
]
```
</details>
