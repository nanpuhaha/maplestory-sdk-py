from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from pydantic import ValidationError

from maplestory.models.union.artifact import (
    ArtifactCrystalRequiredAP,
    UnionArtifact,
    UnionArtifactCrystal,
    UnionArtifactEffect,
    parse_stat_string,
)


class TestParseStatString:
    # Should correctly parse a string with a single stat and return a tuple with the stat name and value
    def test_single_stat_string(self):
        stat_str = "올스탯 150 증가"
        expected_result = ("올스탯", 150)

        result = parse_stat_string(stat_str)
        assert result == expected_result

    # Should correctly parse a string with multiple stats and return a list of tuples with the stat names and values
    def test_parse_stat_string_with_multiple_stats(self):
        stat_str = "공격력 18, 마력 18 증가"
        expected_result = [("공격력", 18), ("마력", 18)]

        result = parse_stat_string(stat_str)
        assert result == expected_result

    # Should correctly parse a string with a decimal percentage value and return a tuple with the stat name and value as a float
    def test_parse_decimal_percentage_value(self):
        stat_str = "몬스터 방어율 무시 20% 증가"
        expected_result = ("몬스터 방어율 무시", 0.2)

        result = parse_stat_string(stat_str)
        assert result == expected_result

    # Should correctly parse a string with a decimal percentage value and return a tuple with the stat name and value as a float
    def test_parse_stat_string_with_percentage_value(self):
        stat_str = "크리티컬 데미지 2.40% 증가"
        expected_result = ("크리티컬 데미지", 0.024)

        result = parse_stat_string(stat_str)
        assert result == expected_result

    # Should raise a ValueError when passed an empty string
    def test_empty_string(self):
        stat_str = ""

        with pytest.raises(ValueError):
            parse_stat_string(stat_str)


class TestUnionArtifactEffect:
    # can be instantiated with a name and level
    def test_instantiation_with_name_and_level(self):
        effect = UnionArtifactEffect(name="올스탯 150 증가", level=10)
        assert effect.name == "올스탯 150 증가"
        assert effect.level == 10

    # can retrieve the parsed stat information from the name property
    def test_retrieve_parsed_stat_information_from_name_property(self):
        effect = UnionArtifactEffect(name="올스탯 150 증가", level=10)
        assert effect.stat == ("올스탯", 150)

    # can check if it is at max level
    def test_is_max_level(self):
        effect = UnionArtifactEffect(name="올스탯 150 증가", level=10)
        assert effect.is_max_level() is True


class TestUnionArtifactCrystal:
    @freeze_time("2024-02-24 12:34:56", tz_offset=9)
    def test_valid_parameters(self):
        crystal = UnionArtifactCrystal(
            name="크리스탈 : 주황버섯",
            validity_flag="0",
            date_expire="2024-03-21T20:21+09:00",
            level=5,
            crystal_option_name_1="버프 지속시간 증가",
            crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
            crystal_option_name_3="몬스터 방어율 무시 증가",
        )

        assert crystal.name == "크리스탈 : 주황버섯"
        assert crystal.active is True
        assert crystal.valid is True
        assert crystal.expired is False
        assert crystal.options == [
            "버프 지속시간 증가",
            "보스 몬스터 공격 시 데미지 증가",
            "몬스터 방어율 무시 증가",
        ]
        assert crystal.option1 == "버프 지속시간 증가"
        assert crystal.option2 == "보스 몬스터 공격 시 데미지 증가"
        assert crystal.option3 == "몬스터 방어율 무시 증가"
        assert crystal.remaining_time == timedelta(days=25, seconds=49564)
        assert crystal.remaining_time_str == "25일 13시간 46분 4초"
        assert crystal.remaining_time_short_str == "25.5일"
        assert crystal.remaining_days == 25

    # create a UnionArtifactCrystal object with a non-string 'name' parameter
    def test_non_string_name(self):
        with pytest.raises(ValidationError):
            _ = UnionArtifactCrystal(
                name=123,
                validity_flag="0",
                date_expire="2024-03-21T20:21+09:00",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            )


class TestArtifactCrystalRequiredAP:
    # Can access the required AP for the next level through the required_ap_for_next_level property
    def test_required_ap_for_next_level(self):
        ap = ArtifactCrystalRequiredAP.LEVEL_1
        assert ap.required_ap_for_next_level == 1

    # Can access the required AP for the max level through the required_ap_for_max_level property
    def test_required_ap_for_max_level(self):
        ap = ArtifactCrystalRequiredAP.LEVEL_1
        assert ap.required_ap_for_max_level == 8 - ap.cumulative

    # Can retrieve an instance of ArtifactCrystalRequiredAP from a given level using the from_level class method
    def test_retrieve_instance_from_level(self):
        ap = ArtifactCrystalRequiredAP.from_level(3)
        assert isinstance(ap, ArtifactCrystalRequiredAP)
        assert ap.cumulative == 3
        assert ap.required == 2

    # Can access the cumulative AP required for a given level through the cumulative attribute of an instance of ArtifactCrystalRequiredAP
    def test_access_cumulative_ap(self):
        ap = ArtifactCrystalRequiredAP.LEVEL_1
        assert ap.cumulative == 0

        ap = ArtifactCrystalRequiredAP.LEVEL_2
        assert ap.cumulative == 1

        ap = ArtifactCrystalRequiredAP.LEVEL_3
        assert ap.cumulative == 3

        ap = ArtifactCrystalRequiredAP.LEVEL_4
        assert ap.cumulative == 5

        ap = ArtifactCrystalRequiredAP.LEVEL_5
        assert ap.cumulative == 8

    # Can access the required AP required for a given level through the required attribute of an instance of ArtifactCrystalRequiredAP
    def test_access_required_ap(self):
        ap = ArtifactCrystalRequiredAP.LEVEL_1
        assert ap.required == 1

        ap = ArtifactCrystalRequiredAP.LEVEL_2
        assert ap.required == 2

        ap = ArtifactCrystalRequiredAP.LEVEL_3
        assert ap.required == 2

        ap = ArtifactCrystalRequiredAP.LEVEL_4
        assert ap.required == 3

        ap = ArtifactCrystalRequiredAP.LEVEL_5
        assert ap.required == 0


class TestUnionArtifact:
    # create a UnionArtifact object with valid data
    def test_valid_data(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.date == date
        assert artifact.effects == effects
        assert artifact.crystals == crystals
        assert artifact.remain_ap == remain_ap

    # create a UnionArtifact object with invalid date format
    def test_invalid_date_format(self):
        date = "2022-01-01"
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        _ = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

    # access the date attribute of a UnionArtifact object
    def test_access_date_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.date == date
        assert artifact.effects == effects
        assert artifact.crystals == crystals
        assert artifact.remain_ap == remain_ap

    # access the effects attribute of a UnionArtifact object
    def test_access_effects_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.effects == effects

    # access the crystals attribute of a UnionArtifact object
    def test_access_crystals_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.crystals == crystals

    # access the remain_ap attribute of a UnionArtifact object
    def test_access_remain_ap_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.remain_ap == remain_ap

    # access the stat attribute of a UnionArtifactEffect object
    def test_access_stat_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.effects[0].stat == parse_stat_string("올스탯 150 증가")
        assert artifact.effects[1].stat == parse_stat_string("데미지 15.00% 증가")
        assert artifact.effects[2].stat == parse_stat_string(
            "보스 몬스터 공격 시 데미지 15.00% 증가"
        )
        assert artifact.effects[0].is_max_level() is True
        assert artifact.effects[1].is_max_level() is True
        assert artifact.effects[2].is_max_level() is True
        assert artifact.effects[0].level == 10
        assert artifact.effects[1].level == 10
        assert artifact.effects[2].level == 10

    # access the option2 attribute of a UnionArtifactCrystal object
    def test_access_option2_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.crystals[0].option2 == "보스 몬스터 공격 시 데미지 증가"
        assert artifact.crystals[1].option2 == "보스 몬스터 공격 시 데미지 증가"

    # access the option1 attribute of a UnionArtifactCrystal object
    def test_access_option1_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.crystals[0].option1 == "버프 지속시간 증가"
        assert artifact.crystals[1].option1 == "버프 지속시간 증가"

    # access the validity_flag attribute of a UnionArtifactCrystal object
    def test_access_validity_flag_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.crystals[0].validity_flag == "0"
        assert artifact.crystals[1].validity_flag == "0"

    # access the level attribute of a UnionArtifactEffect object
    def test_access_level_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.effects[0].level == 10
        assert artifact.effects[1].level == 10
        assert artifact.effects[2].level == 10

    # access the level attribute of a UnionArtifactCrystal object
    def test_access_level_attribute1(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.crystals[0].level == 5
        assert artifact.crystals[1].level == 5

    # access the date_expire attribute of a UnionArtifactCrystal object
    def test_access_date_expire_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.crystals[0].date_expire == crystals[0].date_expire
        assert artifact.crystals[1].date_expire == crystals[1].date_expire

    # access the name attribute of a UnionArtifactCrystal object
    def test_access_name_attribute(self):
        date = datetime.now()
        effects = [
            UnionArtifactEffect(name="올스탯 150 증가", level=10),
            UnionArtifactEffect(name="데미지 15.00% 증가", level=10),
            UnionArtifactEffect(
                name="보스 몬스터 공격 시 데미지 15.00% 증가", level=10
            ),
        ]
        crystals = [
            UnionArtifactCrystal(
                name="크리스탈 : 주황버섯",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
            UnionArtifactCrystal(
                name="크리스탈 : 슬라임",
                validity_flag="0",
                date_expire="2099/01/02 23:59:59:999999",
                level=5,
                crystal_option_name_1="버프 지속시간 증가",
                crystal_option_name_2="보스 몬스터 공격 시 데미지 증가",
                crystal_option_name_3="몬스터 방어율 무시 증가",
            ),
        ]
        remain_ap = 10

        artifact = UnionArtifact(
            date=date,
            union_artifact_effect=effects,
            union_artifact_crystal=crystals,
            union_artifact_remain_ap=remain_ap,
        )

        assert artifact.crystals[0].name == "크리스탈 : 주황버섯"
        assert artifact.crystals[1].name == "크리스탈 : 슬라임"
