import sys

from PIL import Image
from pydantic_core import Url

import maplestory.utils.kst as kst
from maplestory.enums import GradeEnum
from maplestory.models.character.ability import Ability, AbilityPreset
from maplestory.models.character.hyper_stat import HyperStat
from maplestory.models.character.item_equip import (
    CharacterEquipment,
    EquipmentInfo,
    EquipmentTitle,
    ItemAddOption,
    ItemBaseOption,
    ItemEtcOption,
    ItemExceptionalOption,
    ItemStarforceOption,
    ItemTotalOption,
)
from maplestory.models.character.propensity import Propensity
from maplestory.models.character.stat import CharacterStat, CharacterStatInfo
from maplestory.services.character import Character


class TestCharacter:
    # can retrieve basic character information
    def test_retrieve_basic_character_information(self):
        character_name = "온앤온"
        date = kst.datetime(2024, 2, 29)
        character = Character(name=character_name, date=date)
        basic_info = character.basic
        assert basic_info.name == character_name
        assert basic_info.date == date
        assert basic_info.world == "스카니아"
        assert basic_info.gender == "여"
        assert basic_info.job == "아크메이지(썬,콜)"
        assert basic_info.job_level == 6
        assert basic_info.level == 281
        assert basic_info.exp == 3579634472277
        assert basic_info.exp_rate == 9.671
        assert basic_info.guild_name == "온앤온"
        assert isinstance(basic_info.image, Image.Image)

    # can handle missing guild name
    def test_handle_missing_guild_name(self):
        character = Character(name="먼훗날무기상")
        guild_name = character.guild_name
        assert guild_name is None

    # can retrieve character gender
    def test_retrieve_character_gender(self):
        character = Character(name="온앤온")
        assert character.gender == "여"

        character = Character(name="꽁앤꽁")
        assert character.gender == "남"

    # can retrieve character world
    def test_retrieve_character_world(self):
        character = Character(name="온앤온")
        assert character.world == "스카니아"

    # can retrieve character job level
    def test_retrieve_character_job_level(self):
        character = Character(name="온앤온")
        assert character.job_level == 6

    # can retrieve character job
    def test_retrieve_character_job(self):
        character = Character(name="온앤온")
        assert character.job == "아크메이지(썬,콜)"

    # can retrieve character level
    def test_retrieve_character_level(self):
        character = Character(name="온앤온")
        assert isinstance(character.level, int)
        assert 0 < character.level <= 300

        character = Character(name="온앤온", date=kst.datetime(2024, 2, 29))
        assert character.level == 281

    # can retrieve character exp
    def test_retrieve_character_exp(self):
        character = Character(name="온앤온")
        assert isinstance(character.exp, int)
        assert character.exp >= 0

        character = Character(name="온앤온", date=kst.datetime(2024, 2, 29))
        assert character.exp == 3579634472277

    # can retrieve character stat
    def test_retrieve_character_stat(self):
        character = Character(name="온앤온")
        assert isinstance(character.stat, CharacterStat)
        assert character.stat.date == kst.yesterday()

        character = Character(name="온앤온", date=kst.datetime(2024, 2, 29))
        assert isinstance(character.stat, CharacterStat)
        assert character.stat.date == kst.datetime(2024, 2, 29)
        assert character.stat.character_class == "아크메이지(썬,콜)"
        assert character.stat.remain_ap == 0
        assert isinstance(character.stat.stats, list)
        assert isinstance(character.stat.stats[0], CharacterStatInfo)
        assert character.stat.stats == [
            CharacterStatInfo(stat_name="최소 스탯공격력", stat_value=52766830),
            CharacterStatInfo(stat_name="최대 스탯공격력", stat_value=55544030),
            CharacterStatInfo(stat_name="데미지", stat_value=119),
            CharacterStatInfo(stat_name="보스 몬스터 데미지", stat_value=411),
            CharacterStatInfo(stat_name="최종 데미지", stat_value=40),
            CharacterStatInfo(stat_name="방어율 무시", stat_value=96.48),
            CharacterStatInfo(stat_name="크리티컬 확률", stat_value=100),
            CharacterStatInfo(stat_name="크리티컬 데미지", stat_value=73.8),
            CharacterStatInfo(stat_name="상태이상 내성", stat_value=65),
            CharacterStatInfo(stat_name="스탠스", stat_value=100),
            CharacterStatInfo(stat_name="방어력", stat_value=22227),
            CharacterStatInfo(stat_name="이동속도", stat_value=140),
            CharacterStatInfo(stat_name="점프력", stat_value=123),
            CharacterStatInfo(stat_name="스타포스", stat_value=363),
            CharacterStatInfo(stat_name="아케인포스", stat_value=1355),
            CharacterStatInfo(stat_name="어센틱포스", stat_value=430),
            CharacterStatInfo(stat_name="STR", stat_value=5689),
            CharacterStatInfo(stat_name="DEX", stat_value=4825),
            CharacterStatInfo(stat_name="INT", stat_value=62798),
            CharacterStatInfo(stat_name="LUK", stat_value=8069),
            CharacterStatInfo(stat_name="HP", stat_value=25347),
            CharacterStatInfo(stat_name="MP", stat_value=65619),
            CharacterStatInfo(stat_name="AP 배분 STR", stat_value=4),
            CharacterStatInfo(stat_name="AP 배분 DEX", stat_value=4),
            CharacterStatInfo(stat_name="AP 배분 INT", stat_value=1423),
            CharacterStatInfo(stat_name="AP 배분 LUK", stat_value=4),
            CharacterStatInfo(stat_name="AP 배분 HP", stat_value=0),
            CharacterStatInfo(stat_name="AP 배분 MP", stat_value=0),
            CharacterStatInfo(stat_name="아이템 드롭률", stat_value=7),
            CharacterStatInfo(stat_name="메소 획득량", stat_value=4),
            CharacterStatInfo(stat_name="버프 지속시간", stat_value=215),
            CharacterStatInfo(stat_name="공격 속도", stat_value=4),
            CharacterStatInfo(stat_name="일반 몬스터 데미지", stat_value=0),
            CharacterStatInfo(stat_name="재사용 대기시간 감소 (초)", stat_value=0),
            CharacterStatInfo(stat_name="재사용 대기시간 감소 (%)", stat_value=5),
            CharacterStatInfo(stat_name="재사용 대기시간 미적용", stat_value=0),
            CharacterStatInfo(stat_name="속성 내성 무시", stat_value=15),
            CharacterStatInfo(stat_name="상태이상 추가 데미지", stat_value=8),
            CharacterStatInfo(stat_name="무기 숙련도", stat_value=95),
            CharacterStatInfo(stat_name="추가 경험치 획득", stat_value=20),
            CharacterStatInfo(stat_name="공격력", stat_value=2145),
            CharacterStatInfo(stat_name="마력", stat_value=5823),
            CharacterStatInfo(stat_name="전투력", stat_value=140196782),
            CharacterStatInfo(stat_name="소환수 지속시간 증가", stat_value=0),
        ]

    # can retrieve character image
    def test_retrieve_character_image(self):
        character = Character(name="온앤온")
        assert isinstance(character.image, Image.Image)
        assert character.image.size == (96, 96)
        assert character.image.format == "PNG"
        assert character.image.mode == "RGBA"

    # can retrieve character exp rate
    def test_retrieve_character_exp_rate(self):
        character = Character(name="온앤온")
        assert isinstance(character.exp_rate, float)
        assert 0.0 <= character.exp_rate <= 100.0

    # can retrieve character guild name
    def test_retrieve_character_guild_name(self):
        character = Character(name="온앤온")
        assert character.guild_name == "온앤온"

    # can retrieve character propensity
    def test_retrieve_character_propensity(self):
        character = Character(name="온앤온")
        assert isinstance(character.propensity, Propensity)
        assert character.propensity.charisma_level == 100
        assert character.propensity.sensibility_level == 100
        assert character.propensity.insight_level == 100
        assert character.propensity.willingness_level == 100
        assert character.propensity.handicraft_level == 100
        assert character.propensity.charm_level == 100

    # can retrieve character hyper stat
    def test_retrieve_character_hyper_stat(self):
        character = Character(name="온앤온", date=kst.datetime(2024, 2, 29))
        hyper_stat = character.hyper_stat
        assert isinstance(hyper_stat, HyperStat)
        assert hyper_stat.date == kst.datetime(2024, 2, 29)

        # Assertions for the character class and preset number
        assert hyper_stat.character_class == "아크메이지(썬,콜)"
        assert hyper_stat.preset_no == "1"

        # Assertions for use_available and preset1_remain_point for the first preset
        assert hyper_stat.use_available == 1364
        assert hyper_stat.preset1_remain_point == 1

        # Assertions for specific HyperStatItems in preset1
        assert hyper_stat.preset1[2].type == "INT"
        assert hyper_stat.preset1[2].point == 25
        assert hyper_stat.preset1[2].level == 5
        assert hyper_stat.preset1[2].increase == "지력 150 증가"

        assert hyper_stat.preset1[3].type == "LUK"
        assert hyper_stat.preset1[3].point == 3
        assert hyper_stat.preset1[3].level == 2
        assert hyper_stat.preset1[3].increase == "운 60 증가"

        assert hyper_stat.preset1[7].type == "크리티컬 확률"
        assert hyper_stat.preset1[7].point == 85
        assert hyper_stat.preset1[7].level == 8
        assert hyper_stat.preset1[7].increase == "크리티컬 확률 11% 증가"

        # Assertions for preset2_remain_point for the second preset
        assert hyper_stat.preset2_remain_point == 60

        # Assertions for a specific HyperStatItem in preset2
        assert hyper_stat.preset2[8].type == "크리티컬 데미지"
        assert hyper_stat.preset2[8].point == 150
        assert hyper_stat.preset2[8].level == 10
        assert hyper_stat.preset2[8].increase == "크리티컬 데미지 10% 증가"

        # Assertions for preset3_remain_point for the third preset
        assert hyper_stat.preset3_remain_point == 84

        # Assertions for a specific HyperStatItem in preset3
        assert hyper_stat.preset3[8].type == "크리티컬 데미지"
        assert hyper_stat.preset3[8].point == 345
        assert hyper_stat.preset3[8].level == 13
        assert hyper_stat.preset3[8].increase == "크리티컬 데미지 13% 증가"

    # can retrieve character ability
    def test_retrieve_character_ability(self):
        character = Character(name="온앤온")
        ability = character.ability
        assert isinstance(ability, Ability)
        assert ability.date == kst.yesterday()
        if sys.version_info >= (3, 12):
            assert ability.grade in GradeEnum
        else:
            assert ability.grade in GradeEnum.values()
        assert isinstance(ability.info, list)
        assert isinstance(ability.remain_fame, int)
        assert isinstance(ability.preset_no, int)
        assert isinstance(ability.preset1, AbilityPreset)
        assert isinstance(ability.preset2, AbilityPreset)
        assert isinstance(ability.preset3, AbilityPreset)

    # can retrieve character equipment
    def test_retrieve_character_equipment(self):
        character = Character(name="온앤온", date=kst.datetime(2024, 2, 29))
        equipment = character.equipment
        assert isinstance(equipment, CharacterEquipment)
        assert equipment.date == kst.datetime(2024, 2, 29)
        assert equipment.title == EquipmentTitle(
            title_name="예티X핑크빈",
            title_icon="https://open.api.nexon.com/static/maplestory/ItemIcon/KGICLBGC.png",
            title_description="예티와 핑크빈 모두 내 마음 한구석에 남아있네. 예티와 핑크빈을 추억하며.\n올스탯 +20\n최대 HP/최대 MP +1000\n공격력/마력+10\n보스 몬스터 공격 시 데미지+10% \n\n클릭으로 ON/OFF시킬 수 있다.",
            date_expire=None,
            date_option_expire=None,
        )
        assert equipment.preset_no == 2
        assert equipment.character_class == "아크메이지(썬,콜)"
        assert equipment.character_gender == "여"
        assert equipment.mechanic_items == []
        assert equipment.dragon_items == []

        assert isinstance(equipment.items, list)
        first_equip = equipment.items[0]
        assert isinstance(first_equip, EquipmentInfo)
        assert first_equip.part == "모자"
        assert first_equip.slot == "모자"
        assert first_equip.name == "앱솔랩스 메이지크라운"
        assert first_equip.icon == Url(
            "https://open.api.nexon.com/static/maplestory/ItemIcon/KEPCPDMC.png"
        )
        assert first_equip.description is None
        assert first_equip.shape_name == "뾰족귀 모자"
        assert first_equip.shape_icon == Url(
            "https://open.api.nexon.com/static/maplestory/ItemIcon/KEPCPHLG.png"
        )
        assert first_equip.gender is None
        assert first_equip.equipment_level_increase == 0
        assert first_equip.growth_exp == 0
        assert first_equip.growth_level == 0
        assert first_equip.scroll_upgrade == 12
        assert first_equip.cuttable_count == 9
        assert first_equip.golden_hammer_flag is True
        assert first_equip.scroll_resilience_count == 0
        assert first_equip.scroll_upgradeable_count == 0
        assert first_equip.soul_name is None
        assert first_equip.soul_option is None
        assert first_equip.starforce == 22
        assert first_equip.starforce_scroll_flag is False
        assert first_equip.special_ring_level == 0
        assert first_equip.date_expire is None
        assert first_equip.potential_grade == "레전드리"
        assert first_equip.potential_option_1 == "INT : +12%"
        assert first_equip.potential_option_2 == "INT : +9%"
        assert first_equip.potential_option_3 == "INT : +9%"
        assert first_equip.additional_grade == "에픽"
        assert first_equip.additional_option_1 == "마력 : +11"
        assert first_equip.additional_option_2 == "점프력 : +6"
        assert first_equip.additional_option_3 == "마력 : +10"

        # Assertions for total_option
        assert isinstance(first_equip.total_option, ItemTotalOption)
        assert first_equip.total_option.str == 0
        assert first_equip.total_option.int == 341
        assert first_equip.total_option.dex == 0
        assert first_equip.total_option.luk == 176
        assert first_equip.total_option.max_hp == 2295
        assert first_equip.total_option.max_mp == 0
        assert first_equip.total_option.attack_power == 92
        assert first_equip.total_option.magic_power == 102
        assert first_equip.total_option.armor == 1724
        assert first_equip.total_option.speed == 0
        assert first_equip.total_option.jump == 5
        assert first_equip.total_option.boss_damage == 0
        assert first_equip.total_option.ignore_monster_armor == 10
        assert first_equip.total_option.all_stat == 6
        assert first_equip.total_option.damage == 0
        assert first_equip.total_option.max_hp_rate == 0
        assert first_equip.total_option.max_mp_rate == 0
        assert first_equip.total_option.equipment_level_decrease == 0

        # Assertions for base_option
        assert isinstance(first_equip.base_option, ItemBaseOption)
        assert first_equip.base_option.str == 0
        assert first_equip.base_option.int == 45
        assert first_equip.base_option.dex == 0
        assert first_equip.base_option.luk == 45
        assert first_equip.base_option.max_hp == 0
        assert first_equip.base_option.max_mp == 0
        assert first_equip.base_option.attack_power == 0
        assert first_equip.base_option.magic_power == 3
        assert first_equip.base_option.armor == 400
        assert first_equip.base_option.speed == 0
        assert first_equip.base_option.jump == 0
        assert first_equip.base_option.boss_damage == 0
        assert first_equip.base_option.ignore_monster_armor == 10
        assert first_equip.base_option.all_stat == 0
        assert first_equip.base_option.max_hp_rate == 0
        assert first_equip.base_option.max_mp_rate == 0
        assert first_equip.base_option.base_equipment_level == 160

        # Assertions for add_option
        assert isinstance(first_equip.add_option, ItemAddOption)
        assert first_equip.add_option.str == 0
        assert first_equip.add_option.int == 45
        assert first_equip.add_option.dex == 0
        assert first_equip.add_option.luk == 0
        assert first_equip.add_option.max_hp == 0
        assert first_equip.add_option.max_mp == 0
        assert first_equip.add_option.attack_power == 0
        assert first_equip.add_option.magic_power == 6
        assert first_equip.add_option.armor == 0
        assert first_equip.add_option.speed == 0
        assert first_equip.add_option.jump == 5
        assert first_equip.add_option.boss_damage == 0
        assert first_equip.add_option.damage == 0
        assert first_equip.add_option.all_stat == 6
        assert first_equip.add_option.equipment_level_decrease == 0

        # Assertions for etc_option
        assert isinstance(first_equip.etc_option, ItemEtcOption)
        assert first_equip.etc_option.str == 0
        assert first_equip.etc_option.int == 120
        assert first_equip.etc_option.dex == 0
        assert first_equip.etc_option.luk == 0
        assert first_equip.etc_option.max_hp == 2040
        assert first_equip.etc_option.max_mp == 0
        assert first_equip.etc_option.attack_power == 0
        assert first_equip.etc_option.magic_power == 1
        assert first_equip.etc_option.armor == 180
        assert first_equip.etc_option.speed == 0
        assert first_equip.etc_option.jump == 0

        # Assertions for exceptional_option
        assert isinstance(first_equip.exceptional_option, ItemExceptionalOption)
        assert first_equip.exceptional_option.str == 0
        assert first_equip.exceptional_option.int == 0
        assert first_equip.exceptional_option.dex == 0
        assert first_equip.exceptional_option.luk == 0
        assert first_equip.exceptional_option.max_hp == 0
        assert first_equip.exceptional_option.max_mp == 0
        assert first_equip.exceptional_option.attack_power == 0
        assert first_equip.exceptional_option.magic_power == 0

        # Assertions for starforce_option
        assert isinstance(first_equip.starforce_option, ItemStarforceOption)
        assert first_equip.starforce_option.str == 0
        assert first_equip.starforce_option.int == 131
        assert first_equip.starforce_option.dex == 0
        assert first_equip.starforce_option.luk == 131
        assert first_equip.starforce_option.max_hp == 255
        assert first_equip.starforce_option.max_mp == 0
        assert first_equip.starforce_option.attack_power == 92
        assert first_equip.starforce_option.magic_power == 92
        assert first_equip.starforce_option.armor == 1144
        assert first_equip.starforce_option.speed == 0
        assert first_equip.starforce_option.jump == 0

        assert isinstance(equipment.preset1, list)
        assert isinstance(equipment.preset1[0], EquipmentInfo)

        assert isinstance(equipment.preset2, list)
        assert isinstance(equipment.preset2[0], EquipmentInfo)

        assert isinstance(equipment.preset3, list)
        assert isinstance(equipment.preset3[0], EquipmentInfo)
