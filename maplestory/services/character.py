from datetime import datetime
from enum import Enum

from PIL import Image
from pydantic import BaseModel, ConfigDict, computed_field

from maplestory.apis.character import (
    get_basic_character_info_by_ocid,
    get_character_ability_by_ocid,
    get_character_android_equipment_by_ocid,
    get_character_beauty_equipment_by_ocid,
    get_character_cashitem_equipment_by_ocid,
    get_character_dojang_record_by_ocid,
    get_character_equipment_by_ocid,
    get_character_hexamatrix_by_ocid,
    get_character_hexamatrix_stat_by_ocid,
    get_character_hyper_stat_by_ocid,
    get_character_link_skill_by_ocid,
    get_character_ocid,
    get_character_pet_equipment_by_ocid,
    get_character_propensity_by_ocid,
    get_character_set_effect_by_ocid,
    get_character_skill_by_ocid,
    get_character_stat_by_ocid,
    get_character_symbol_equipment_by_ocid,
    get_character_vmatrix_by_ocid,
    get_popularity_by_ocid,
)
from maplestory.models.character import (
    Ability,
    AndroidEquipment,
    BeautyEquipment,
    CashitemEquipment,
    CharacterBasic,
    CharacterDojang,
    CharacterEquipment,
    CharacterLinkSkill,
    CharacterPet,
    CharacterSkill,
    CharacterStat,
    HexaMatrix,
    HexaMatrixStat,
    HyperStat,
    Popularity,
    Propensity,
    SetEffect,
    SymbolEquipment,
    VMatrix,
)
from maplestory.services.guild import Guild
from maplestory.utils.kst import yesterday
from maplestory.utils.repr import DatetimeRepresentation


class Character(DatetimeRepresentation, BaseModel):
    """캐릭터 식별자(ocid)

    Attributes:
        name: 캐릭터명
        date: 조회 기준일 (KST)
    """

    name: str
    date: datetime = yesterday()

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # region id

    @computed_field(repr=False)
    def id(self) -> str:
        return get_character_id(self.name)

    ocid = id

    # endregion

    # region basic

    @computed_field(repr=False)
    @property
    def basic(self) -> CharacterBasic:
        return get_basic_character_info(self.name, self.date)

    @computed_field
    def world(self) -> str:
        return self.basic.world

    @computed_field
    def gender(self) -> str:
        return self.basic.gender

    @computed_field
    def job(self) -> str:
        return self.basic.job

    @computed_field
    def job_level(self) -> int:
        return self.basic.job_level

    @computed_field
    def level(self) -> int:
        return self.basic.level

    @computed_field
    def exp(self) -> int:
        return self.basic.exp

    @computed_field
    def exp_rate(self) -> float:
        return self.basic.exp_rate

    @computed_field
    def guild_name(self) -> str | None:
        return self.basic.guild_name

    @computed_field(repr=False)
    def image(self) -> Image.Image:
        return self.basic.image

    # endregion

    # region guild

    @property
    def guild(self) -> Guild:
        return Guild(name=self.basic.guild_name, world=self.basic.world)

    # endregion

    # region popularity

    @computed_field
    def popularity(self) -> int:
        return get_popularity(self.name, self.date).popularity

    # endregion

    @computed_field(repr=False)
    def stat(self) -> CharacterStat:
        return get_character_stat(self.name, self.date)

    @property
    def hyper_stat(self) -> HyperStat:
        return get_character_hyper_stat(self.name, self.date)

    @property
    def propensity(self) -> Propensity:
        return get_character_propensity(self.name, self.date)

    @property
    def ability(self) -> Ability:
        return get_character_ability(self.name, self.date)

    @property
    def equipment(self) -> CharacterEquipment:
        return get_character_equipment(self.name, self.date)

    @property
    def cashitem_equipment(self) -> CashitemEquipment:
        return get_character_cashitem_equipment(self.name, self.date)

    @property
    def symbol_equipment(self) -> SymbolEquipment:
        return get_character_symbol_equipment(self.name, self.date)

    @property
    def set_effect(self) -> SetEffect:
        return get_character_set_effect(self.name, self.date)

    @property
    def beauty_equipment(self) -> BeautyEquipment:
        return get_character_beauty_equipment(self.name, self.date)

    @property
    def android_equipment(self) -> AndroidEquipment:
        return get_character_android_equipment(self.name, self.date)

    @property
    def pet_equipment(self) -> CharacterPet:
        return get_character_pet_equipment(self.name, self.date)

    @property
    def skill_0th(self) -> CharacterSkill:
        return get_character_skill(self.name, 0, self.date)

    @property
    def skill_1st(self) -> CharacterSkill:
        return get_character_skill(self.name, 1, self.date)

    @property
    def skill_2nd(self) -> CharacterSkill:
        return get_character_skill(self.name, 2, self.date)

    @property
    def skill_3rd(self) -> CharacterSkill:
        return get_character_skill(self.name, 3, self.date)

    @property
    def skill_4th(self) -> CharacterSkill:
        return get_character_skill(self.name, 4, self.date)

    @property
    def skill_5th(self) -> CharacterSkill:
        return get_character_skill(self.name, 5, self.date)

    @property
    def skill_6th(self) -> CharacterSkill:
        return get_character_skill(self.name, 6, self.date)

    @property
    def link_skill(self) -> CharacterLinkSkill:
        return get_character_link_skill(self.name, self.date)

    @property
    def vmatrix(self) -> VMatrix:
        return get_character_vmatrix(self.name, self.date)

    @property
    def hexamatrix(self) -> HexaMatrix:
        return get_character_hexamatrix(self.name, self.date)

    @property
    def hexamatrix_stat(self) -> HexaMatrixStat:
        return get_character_hexamatrix_stat(self.name, self.date)

    @property
    def dojang_record(self) -> CharacterDojang:
        return get_character_dojang_record(self.name, self.date)

    def required_exp_for_level(self, target_level: int) -> int:
        now_culmulative = CharacterExperience.from_level(self.basic.level).culmulative
        target_culmulative = CharacterExperience.from_level(target_level).culmulative
        required_exp = target_culmulative - now_culmulative - self.basic.exp
        return max(required_exp, 0)

    특정레벨까지필요한경험치 = required_exp_for_level


class CharacterExperience(Enum):
    LEVEL_1 = (0, 15)
    LEVEL_2 = (15, 34)
    LEVEL_3 = (49, 57)
    LEVEL_4 = (106, 92)
    LEVEL_5 = (198, 135)
    LEVEL_6 = (333, 372)
    LEVEL_7 = (705, 560)
    LEVEL_8 = (1_265, 840)
    LEVEL_9 = (2_105, 1_242)
    LEVEL_10 = (3_347, 1_242)
    LEVEL_11 = (4_589, 1_242)
    LEVEL_12 = (5_831, 1_242)
    LEVEL_13 = (7_073, 1_242)
    LEVEL_14 = (8_315, 1_242)
    LEVEL_15 = (9_557, 1_490)
    LEVEL_16 = (11_047, 1_788)
    LEVEL_17 = (12_835, 2_145)
    LEVEL_18 = (14_980, 2_574)
    LEVEL_19 = (17_554, 3_088)
    LEVEL_20 = (20_642, 3_705)
    LEVEL_21 = (24_347, 4_446)
    LEVEL_22 = (28_793, 5_335)
    LEVEL_23 = (34_128, 6_402)
    LEVEL_24 = (40_530, 7_682)
    LEVEL_25 = (48_212, 9_218)
    LEVEL_26 = (57_430, 11_061)
    LEVEL_27 = (68_491, 13_273)
    LEVEL_28 = (81_764, 15_927)
    LEVEL_29 = (97_691, 19_112)
    LEVEL_30 = (116_803, 19_112)
    LEVEL_31 = (135_915, 19_112)
    LEVEL_32 = (155_027, 19_112)
    LEVEL_33 = (174_139, 19_112)
    LEVEL_34 = (193_251, 19_112)
    LEVEL_35 = (212_363, 22_934)
    LEVEL_36 = (235_297, 27_520)
    LEVEL_37 = (262_817, 33_024)
    LEVEL_38 = (295_841, 39_628)
    LEVEL_39 = (335_469, 47_553)
    LEVEL_40 = (383_022, 51_357)
    LEVEL_41 = (434_379, 55_465)
    LEVEL_42 = (489_844, 59_902)
    LEVEL_43 = (549_746, 64_694)
    LEVEL_44 = (614_440, 69_869)
    LEVEL_45 = (684_309, 75_458)
    LEVEL_46 = (759_767, 81_494)
    LEVEL_47 = (841_261, 88_013)
    LEVEL_48 = (929_274, 95_054)
    LEVEL_49 = (1_024_328, 102_658)
    LEVEL_50 = (1_126_986, 110_870)
    LEVEL_51 = (1_237_856, 119_739)
    LEVEL_52 = (1_357_595, 129_318)
    LEVEL_53 = (1_486_913, 139_663)
    LEVEL_54 = (1_626_576, 150_836)
    LEVEL_55 = (1_777_412, 162_902)
    LEVEL_56 = (1_940_314, 175_934)
    LEVEL_57 = (2_116_248, 190_008)
    LEVEL_58 = (2_306_256, 205_208)
    LEVEL_59 = (2_511_464, 221_624)
    LEVEL_60 = (2_733_088, 221_624)
    LEVEL_61 = (2_954_712, 221_624)
    LEVEL_62 = (3_176_336, 221_624)
    LEVEL_63 = (3_397_960, 221_624)
    LEVEL_64 = (3_619_584, 221_624)
    LEVEL_65 = (3_841_208, 238_245)
    LEVEL_66 = (4_079_453, 256_113)
    LEVEL_67 = (4_335_566, 275_321)
    LEVEL_68 = (4_610_887, 295_970)
    LEVEL_69 = (4_906_857, 318_167)
    LEVEL_70 = (5_225_024, 342_029)
    LEVEL_71 = (5_567_053, 367_681)
    LEVEL_72 = (5_934_734, 395_257)
    LEVEL_73 = (6_329_991, 424_901)
    LEVEL_74 = (6_754_892, 456_768)
    LEVEL_75 = (7_211_660, 488_741)
    LEVEL_76 = (7_700_401, 522_952)
    LEVEL_77 = (8_223_353, 559_558)
    LEVEL_78 = (8_782_911, 598_727)
    LEVEL_79 = (9_381_638, 640_637)
    LEVEL_80 = (10_022_275, 685_481)
    LEVEL_81 = (10_707_756, 733_464)
    LEVEL_82 = (11_441_220, 784_806)
    LEVEL_83 = (12_226_026, 839_742)
    LEVEL_84 = (13_065_768, 898_523)
    LEVEL_85 = (13_964_291, 961_419)
    LEVEL_86 = (14_925_710, 1_028_718)
    LEVEL_87 = (15_954_428, 1_100_728)
    LEVEL_88 = (17_055_156, 1_177_778)
    LEVEL_89 = (18_232_934, 1_260_222)
    LEVEL_90 = (19_493_156, 1_342_136)
    LEVEL_91 = (20_835_292, 1_429_374)
    LEVEL_92 = (22_264_666, 1_522_283)
    LEVEL_93 = (23_786_949, 1_621_231)
    LEVEL_94 = (25_408_180, 1_726_611)
    LEVEL_95 = (27_134_791, 1_838_840)
    LEVEL_96 = (28_973_631, 1_958_364)
    LEVEL_97 = (30_931_995, 2_085_657)
    LEVEL_98 = (33_017_652, 2_221_224)
    LEVEL_99 = (35_238_876, 2_365_603)
    LEVEL_100 = (37_604_479, 2_365_603)
    LEVEL_101 = (39_970_082, 2_365_603)
    LEVEL_102 = (42_335_685, 2_365_603)
    LEVEL_103 = (44_701_288, 2_365_603)
    LEVEL_104 = (47_066_891, 2_365_603)
    LEVEL_105 = (49_432_494, 2_519_367)
    LEVEL_106 = (51_951_861, 2_683_125)
    LEVEL_107 = (54_634_986, 2_857_528)
    LEVEL_108 = (57_492_514, 3_043_267)
    LEVEL_109 = (60_535_781, 3_241_079)
    LEVEL_110 = (63_776_860, 3_451_749)
    LEVEL_111 = (67_228_609, 3_676_112)
    LEVEL_112 = (70_904_721, 3_915_059)
    LEVEL_113 = (74_819_780, 4_169_537)
    LEVEL_114 = (78_989_317, 4_440_556)
    LEVEL_115 = (83_429_873, 4_729_192)
    LEVEL_116 = (88_159_065, 5_036_589)
    LEVEL_117 = (93_195_654, 5_363_967)
    LEVEL_118 = (98_559_621, 5_712_624)
    LEVEL_119 = (104_272_245, 6_083_944)
    LEVEL_120 = (110_356_189, 6_479_400)
    LEVEL_121 = (116_835_589, 6_900_561)
    LEVEL_122 = (123_736_150, 7_349_097)
    LEVEL_123 = (131_085_247, 7_826_788)
    LEVEL_124 = (138_912_035, 8_335_529)
    LEVEL_125 = (147_247_564, 8_877_338)
    LEVEL_126 = (156_124_902, 9_454_364)
    LEVEL_127 = (165_579_266, 10_068_897)
    LEVEL_128 = (175_648_163, 10_723_375)
    LEVEL_129 = (186_371_538, 11_420_394)
    LEVEL_130 = (197_791_932, 12_162_719)
    LEVEL_131 = (209_954_651, 12_953_295)
    LEVEL_132 = (222_907_946, 13_795_259)
    LEVEL_133 = (236_703_205, 14_691_950)
    LEVEL_134 = (251_395_155, 15_646_926)
    LEVEL_135 = (267_042_081, 16_663_976)
    LEVEL_136 = (283_706_057, 17_747_134)
    LEVEL_137 = (301_453_191, 18_900_697)
    LEVEL_138 = (320_353_888, 20_129_242)
    LEVEL_139 = (340_483_130, 21_437_642)
    LEVEL_140 = (361_920_772, 22_777_494)
    LEVEL_141 = (384_698_266, 24_201_087)
    LEVEL_142 = (408_899_353, 25_713_654)
    LEVEL_143 = (434_613_007, 27_320_757)
    LEVEL_144 = (461_933_764, 29_028_304)
    LEVEL_145 = (490_962_068, 30_842_573)
    LEVEL_146 = (521_804_641, 32_770_233)
    LEVEL_147 = (554_574_874, 34_818_372)
    LEVEL_148 = (589_393_246, 36_994_520)
    LEVEL_149 = (626_387_766, 39_306_677)
    LEVEL_150 = (665_694_443, 41_763_344)
    LEVEL_151 = (707_457_787, 44_373_553)
    LEVEL_152 = (751_831_340, 47_146_900)
    LEVEL_153 = (798_978_240, 50_093_581)
    LEVEL_154 = (849_071_821, 53_224_429)
    LEVEL_155 = (902_296_250, 56_550_955)
    LEVEL_156 = (958_847_205, 60_085_389)
    LEVEL_157 = (1_018_932_594, 63_840_725)
    LEVEL_158 = (1_082_773_319, 67_830_770)
    LEVEL_159 = (1_150_604_089, 72_070_193)
    LEVEL_160 = (1_222_674_282, 76_574_580)
    LEVEL_161 = (1_299_248_862, 81_360_491)
    LEVEL_162 = (1_380_609_353, 86_445_521)
    LEVEL_163 = (1_467_054_874, 91_848_366)
    LEVEL_164 = (1_558_903_240, 97_588_888)
    LEVEL_165 = (1_656_492_128, 103_688_193)
    LEVEL_166 = (1_760_180_321, 110_168_705)
    LEVEL_167 = (1_870_349_026, 117_054_249)
    LEVEL_168 = (1_987_403_275, 124_370_139)
    LEVEL_169 = (2_111_773_414, 132_143_272)
    LEVEL_170 = (2_243_916_686, 138_750_435)
    LEVEL_171 = (2_382_667_121, 145_687_956)
    LEVEL_172 = (2_528_355_077, 152_972_353)
    LEVEL_173 = (2_681_327_430, 160_620_970)
    LEVEL_174 = (2_841_948_400, 168_652_018)
    LEVEL_175 = (3_010_600_418, 177_084_618)
    LEVEL_176 = (3_187_685_036, 185_938_848)
    LEVEL_177 = (3_373_623_884, 195_235_790)
    LEVEL_178 = (3_568_859_674, 204_997_579)
    LEVEL_179 = (3_773_857_253, 215_247_457)
    LEVEL_180 = (3_989_104_710, 226_009_829)
    LEVEL_181 = (4_215_114_539, 237_310_320)
    LEVEL_182 = (4_452_424_859, 249_175_836)
    LEVEL_183 = (4_701_600_695, 261_634_627)
    LEVEL_184 = (4_963_235_322, 274_716_358)
    LEVEL_185 = (5_237_951_680, 288_452_175)
    LEVEL_186 = (5_526_403_855, 302_874_783)
    LEVEL_187 = (5_829_278_638, 318_018_522)
    LEVEL_188 = (6_147_297_160, 333_919_448)
    LEVEL_189 = (6_481_216_608, 350_615_420)
    LEVEL_190 = (6_831_832_028, 368_146_191)
    LEVEL_191 = (7_199_978_219, 386_553_500)
    LEVEL_192 = (7_586_531_719, 405_881_175)
    LEVEL_193 = (7_992_412_894, 426_175_233)
    LEVEL_194 = (8_418_588_127, 447_483_994)
    LEVEL_195 = (8_866_072_121, 469_858_193)
    LEVEL_196 = (9_335_930_314, 493_351_102)
    LEVEL_197 = (9_829_281_416, 518_018_657)
    LEVEL_198 = (10_347_300_073, 543_919_589)
    LEVEL_199 = (10_891_219_662, 571_115_568)
    LEVEL_200 = (11_462_335_230, 2_207_026_470)
    LEVEL_201 = (13_669_361_700, 2_471_869_646)
    LEVEL_202 = (16_141_231_346, 2_768_494_003)
    LEVEL_203 = (18_909_725_349, 3_100_713_283)
    LEVEL_204 = (22_010_438_632, 3_472_798_876)
    LEVEL_205 = (25_483_237_508, 3_889_534_741)
    LEVEL_206 = (29_372_772_249, 4_356_278_909)
    LEVEL_207 = (33_729_051_158, 4_879_032_378)
    LEVEL_208 = (38_608_083_536, 5_464_516_263)
    LEVEL_209 = (44_072_599_799, 6_120_258_214)
    LEVEL_210 = (50_192_858_013, 7_956_335_678)
    LEVEL_211 = (58_149_193_691, 8_831_532_602)
    LEVEL_212 = (66_980_726_293, 9_803_001_188)
    LEVEL_213 = (76_783_727_481, 10_881_331_318)
    LEVEL_214 = (87_665_058_799, 12_078_277_762)
    LEVEL_215 = (99_743_336_561, 15_701_761_090)
    LEVEL_216 = (115_445_097_651, 17_114_919_588)
    LEVEL_217 = (132_560_017_239, 18_655_262_350)
    LEVEL_218 = (151_215_279_589, 20_334_235_961)
    LEVEL_219 = (171_549_515_550, 22_164_317_197)
    LEVEL_220 = (193_713_832_747, 28_813_612_356)
    LEVEL_221 = (222_527_445_103, 30_830_565_220)
    LEVEL_222 = (253_358_010_323, 32_988_704_785)
    LEVEL_223 = (286_346_715_108, 35_297_914_119)
    LEVEL_224 = (321_644_629_227, 37_768_768_107)
    LEVEL_225 = (359_413_397_334, 49_099_398_539)
    LEVEL_226 = (408_512_795_873, 52_536_356_436)
    LEVEL_227 = (461_049_152_309, 56_213_901_386)
    LEVEL_228 = (517_263_053_695, 60_148_874_483)
    LEVEL_229 = (577_411_928_178, 64_359_295_696)
    LEVEL_230 = (641_771_223_874, 83_667_084_404)
    LEVEL_231 = (725_438_308_278, 86_177_096_936)
    LEVEL_232 = (811_615_405_214, 88_762_409_844)
    LEVEL_233 = (900_377_815_058, 91_425_282_139)
    LEVEL_234 = (991_803_097_197, 94_168_040_603)
    LEVEL_235 = (1_085_971_137_800, 122_418_452_783)
    LEVEL_236 = (1_208_389_590_583, 126_091_006_366)
    LEVEL_237 = (1_334_480_596_949, 129_873_736_556)
    LEVEL_238 = (1_464_354_333_505, 133_769_948_652)
    LEVEL_239 = (1_598_124_282_157, 137_783_047_111)
    LEVEL_240 = (1_735_907_329_268, 179_117_961_244)
    LEVEL_241 = (1_915_025_290_512, 184_491_500_081)
    LEVEL_242 = (2_099_516_790_593, 190_026_245_083)
    LEVEL_243 = (2_289_543_035_676, 195_727_032_435)
    LEVEL_244 = (2_485_270_068_111, 201_598_843_408)
    LEVEL_245 = (2_686_868_911_519, 262_078_496_430)
    LEVEL_246 = (2_948_947_407_949, 269_940_851_322)
    LEVEL_247 = (3_218_888_259_271, 278_039_076_861)
    LEVEL_248 = (3_496_927_336_132, 286_380_249_166)
    LEVEL_249 = (3_783_307_585_298, 294_971_656_640)
    LEVEL_250 = (4_078_279_241_938, 442_457_484_960)
    LEVEL_251 = (4_520_736_726_898, 455_731_209_508)
    LEVEL_252 = (4_976_467_936_406, 469_403_145_793)
    LEVEL_253 = (5_445_871_082_199, 483_485_240_166)
    LEVEL_254 = (5_929_356_322_365, 497_989_797_370)
    LEVEL_255 = (6_427_346_119_735, 512_929_491_291)
    LEVEL_256 = (6_940_275_611_026, 528_317_376_029)
    LEVEL_257 = (7_468_592_987_055, 544_166_897_309)
    LEVEL_258 = (8_012_759_884_364, 560_491_904_228)
    LEVEL_259 = (8_573_251_788_592, 577_306_661_354)
    LEVEL_260 = (9_150_558_449_946, 1_731_919_984_062)
    LEVEL_261 = (10_882_478_434_008, 1_749_239_183_902)
    LEVEL_262 = (12_631_717_617_910, 1_766_731_575_741)
    LEVEL_263 = (14_398_449_193_651, 1_784_398_891_498)
    LEVEL_264 = (16_182_848_085_149, 1_802_242_880_412)
    LEVEL_265 = (17_985_090_965_561, 2_342_915_744_535)
    LEVEL_266 = (20_328_006_710_096, 2_366_344_901_980)
    LEVEL_267 = (22_694_351_612_076, 2_390_008_350_999)
    LEVEL_268 = (25_084_359_963_075, 2_413_908_434_508)
    LEVEL_269 = (27_498_268_397_583, 2_438_047_518_853)
    LEVEL_270 = (29_936_315_916_436, 5_412_465_491_853)
    LEVEL_271 = (35_348_781_408_289, 5_466_590_146_771)
    LEVEL_272 = (40_815_371_555_060, 5_521_256_048_238)
    LEVEL_273 = (46_336_627_603_298, 5_576_468_608_720)
    LEVEL_274 = (51_913_096_212_018, 5_632_233_294_807)
    LEVEL_275 = (57_545_329_506_825, 11_377_111_255_510)
    LEVEL_276 = (68_922_440_762_335, 12_514_822_381_061)
    LEVEL_277 = (81_437_263_143_396, 13_766_304_619_167)
    LEVEL_278 = (95_203_567_762_563, 15_142_935_081_083)
    LEVEL_279 = (110_346_502_843_646, 16_657_228_589_191)
    LEVEL_280 = (127_003_731_432_837, 33_647_601_750_165)
    LEVEL_281 = (160_651_333_183_002, 37_012_361_925_181)
    LEVEL_282 = (197_663_695_108_183, 40_713_598_117_699)
    LEVEL_283 = (238_377_293_225_882, 44_784_957_929_468)
    LEVEL_284 = (283_162_251_155_350, 49_263_453_722_414)
    LEVEL_285 = (332_425_704_877_764, 99_512_176_519_276)
    LEVEL_286 = (431_937_881_397_040, 109_463_394_171_203)
    LEVEL_287 = (541_401_275_568_243, 120_409_733_588_323)
    LEVEL_288 = (661_811_009_156_566, 132_450_706_947_155)
    LEVEL_289 = (794_261_716_103_721, 145_695_777_641_870)
    LEVEL_290 = (939_957_493_745_591, 294_305_470_836_577)
    LEVEL_291 = (1_234_262_964_582_168, 323_736_017_920_234)
    LEVEL_292 = (1_557_998_982_502_402, 356_109_619_712_257)
    LEVEL_293 = (1_914_108_602_214_659, 391_720_581_683_482)
    LEVEL_294 = (2_305_829_183_898_141, 430_892_639_851_830)
    LEVEL_295 = (2_736_721_823_749_971, 870_403_132_500_696)
    LEVEL_296 = (3_607_124_956_250_667, 957_443_445_750_765)
    LEVEL_297 = (4_564_568_402_001_432, 1_053_187_790_325_841)
    LEVEL_298 = (5_617_756_192_327_273, 1_158_506_569_358_425)
    LEVEL_299 = (6_776_262_761_685_698, 1_737_759_854_037_637)
    LEVEL_300 = (8_514_022_615_723_335, 0)

    def __init__(self, cumulative, required):
        self.cumulative = cumulative
        self.required = required

    @classmethod
    def from_level(cls, level: int):
        key = f"LEVEL_{level}"
        return cls[key]

    @property
    def required_exp_for_next_level(self) -> int:
        return self.required

    @property
    def required_exp_for_max_level(self) -> int:
        return self.__class__.LEVEL_300.cumulative - self.cumulative


def get_character_id(character_name: str) -> str:
    """
    캐릭터의 식별자(ocid)를 조회합니다.
    Fetches the identifier (ocid) of a character.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.

    Returns:
        str: 주어진 이름의 캐릭터 식별자.
             The character with the given name.

    Note:
        - 2023년 12월 21일부터 데이터를 조회할 수 있습니다.
          Data can be queried from December 21, 2023.
        - 캐릭터 정보 조회 API는 일자별 데이터로 매일 오전 1시부터 전일 데이터 조회가 가능합니다.
          The character information query API provides daily data, and data for the previous day can be queried from 1 AM every day.
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
          The ocid may change due to game content changes. Please be careful when updating services based on ocid.
    """

    return get_character_ocid(character_name)


def get_basic_character_info(
    character_name: str,
    date: datetime = yesterday(),
) -> CharacterBasic:
    """
    캐릭터의 기본 정보를 조회합니다.
    Fetches the basic information of a character.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterBasic: 캐릭터의 기본 정보.
                        The basic information of the character.

    Note:
        - 2023년 12월 21일부터 데이터를 조회할 수 있습니다.
          Data can be queried from December 21, 2023.
        - 캐릭터 정보 조회 API는 일자별 데이터로 매일 오전 1시부터 전일 데이터 조회가 가능합니다. (예를 들어, 12월 22일 데이터를 조회하면 22일 00시부터 23일의 00시 사이의 데이터가 조회됩니다.)
          The character information query API provides daily data, and data for the previous day can be queried from 1 AM every day. (For example, if you query data for December 22, you will get data from 00:00 on the 22nd to 00:00 on the 23rd.)
        - 게임 콘텐츠 변경으로 ocid가 변경될 수 있습니다. ocid 기반 서비스 갱신 시 유의해 주시길 바랍니다.
          The ocid may change due to game content changes. Please be careful when updating services based on ocid.
    """

    character_ocid = get_character_id(character_name)
    return get_basic_character_info_by_ocid(character_ocid, date)


def get_popularity(
    character_name: str,
    date: datetime = yesterday(),
) -> Popularity:
    """
    캐릭터의 인기도 정보를 조회합니다.
    Fetches the popularity information of a character.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterPopularity: 캐릭터의 인기도 정보.
                             The popularity information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_popularity_by_ocid(character_ocid, date)


def get_character_stat(
    character_name: str,
    date: datetime = yesterday(),
) -> CharacterStat:
    """
    캐릭터의 종합능력치 정보를 조회합니다.
    Fetches the comprehensive ability information of a character.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterStat: 캐릭터의 종합능력치 정보.
                       The comprehensive ability information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_stat_by_ocid(character_ocid, date)


def get_character_hyper_stat(
    character_name: str,
    date: datetime = yesterday(),
) -> HyperStat:
    """
    캐릭터의 하이퍼스탯 정보를 조회합니다.
    Fetches the hyper stat information of a character.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterHyperStat: 캐릭터의 하이퍼스탯 정보.
                            The hyper stat information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_hyper_stat_by_ocid(character_ocid, date)


def get_character_propensity(
    character_name: str,
    date: datetime = yesterday(),
) -> Propensity:
    """
    캐릭터의 성향 정보를 조회합니다.
    Fetches the propensity information of a character.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterPropensity: 캐릭터의 성향 정보.
                             The propensity information of the character.
    """
    character_ocid = get_character_id(character_name)
    return get_character_propensity_by_ocid(character_ocid, date)


def get_character_ability(
    character_name: str,
    date: datetime = yesterday(),
) -> Ability:
    """
    캐릭터의 어빌리티 정보를 조회합니다.
    Fetches the ability information of a character.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterAbility: 캐릭터의 어빌리티 정보.
                          The ability information of the character.
    """
    character_ocid = get_character_id(character_name)
    return get_character_ability_by_ocid(character_ocid, date)


def get_character_equipment(
    character_name: str,
    date: datetime = yesterday(),
) -> CharacterEquipment:
    """
    장착한 장비 중 캐시 장비를 제외한 나머지 장비 정보를 조회합니다.
    Fetches the information of equipped items excluding cash items.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterItemEquipment: 캐릭터의 장비 정보.
                                The equipment information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_equipment_by_ocid(character_ocid, date)


def get_character_cashitem_equipment(
    character_name: str,
    date: datetime = yesterday(),
) -> CashitemEquipment:
    """
    장착한 캐시 장비 정보를 조회합니다.
    Fetches the information of equipped cash items.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterCashitemEquipment: 캐릭터의 캐시 장비 정보.
                                    The cash item equipment information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_cashitem_equipment_by_ocid(character_ocid, date)


def get_character_symbol_equipment(
    character_name: str,
    date: datetime = yesterday(),
) -> SymbolEquipment:
    """
    장착한 심볼 정보를 조회합니다.
    Fetches the equipped symbol information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterSymbolEquipment: 캐릭터의 심볼 장비 정보.
                                  The symbol equipment information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_symbol_equipment_by_ocid(character_ocid, date)


def get_character_set_effect(
    character_name: str,
    date: datetime = yesterday(),
) -> SetEffect:
    """
    적용받고 있는 세트 효과 정보를 조회합니다.
    Fetches the applied set effect information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterSetEffect: 캐릭터의 세트 효과 정보.
                            The set effect information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_set_effect_by_ocid(character_ocid, date)


def get_character_beauty_equipment(
    character_name: str,
    date: datetime = yesterday(),
) -> BeautyEquipment:
    """
    캐릭터 헤어, 성형, 피부 정보를 조회합니다.
    Fetches the character's hair, plastic surgery, and skin information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterBeautyEquipment: 캐릭터의 미용 장비 정보.
                                  The beauty equipment information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_beauty_equipment_by_ocid(character_ocid, date)


def get_character_android_equipment(
    character_name: str,
    date: datetime = yesterday(),
) -> AndroidEquipment:
    """
    장착한 안드로이드 정보를 조회합니다.
    Fetches the equipped android information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterAndroidEquipment: 캐릭터의 안드로이드 장비 정보.
                                   The android equipment information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_android_equipment_by_ocid(character_ocid, date)


def get_character_pet_equipment(
    character_name: str,
    date: datetime = yesterday(),
) -> CharacterPet:
    """
    장착한 펫 및 펫 스킬, 장비 정보를 조회합니다.
    Fetches the equipped pet and pet skill, equipment information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterPetEquipment: 캐릭터의 펫 장비 정보.
                               The pet equipment information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_pet_equipment_by_ocid(character_ocid, date)


def get_character_skill(
    character_name: str,
    skill_grade: int,
    date: datetime = yesterday(),
) -> CharacterSkill:
    """
    캐릭터 스킬과 하이퍼 스킬 정보를 조회합니다.
    Fetches the character's skill and hyper skill information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        skill_grade : 조회하고자 하는 전직 차수.
                      The job advancement grade to query.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterSkill: 캐릭터의 스킬 정보.
                        The skill information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_skill_by_ocid(character_ocid, skill_grade, date)


def get_character_link_skill(
    character_name: str,
    date: datetime = yesterday(),
) -> CharacterLinkSkill:
    """
    장착 링크 스킬 정보를 조회합니다.
    Fetches the equipped link skill information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterLinkSkill: 캐릭터의 링크 스킬 정보.
                            The link skill information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_link_skill_by_ocid(character_ocid, date)


def get_character_vmatrix(
    character_name: str,
    date: datetime = yesterday(),
) -> VMatrix:
    """
    V매트릭스 슬롯 정보와 장착한 V코어 정보를 조회합니다.
    Fetches the VMatrix slot information and the equipped VCore information.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterVMatrix: 캐릭터의 V매트릭스 정보.
                          The VMatrix information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_vmatrix_by_ocid(character_ocid, date)


def get_character_hexamatrix(
    character_name: str,
    date: datetime = yesterday(),
) -> HexaMatrix:
    """
    HEXA 매트릭스에 장착한 HEXA 코어 정보를 조회합니다.
    Fetches the HEXA core information equipped in the HEXA matrix.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterHexaMatrix: 캐릭터의 HEXA 매트릭스 정보.
                             The HEXA matrix information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_hexamatrix_by_ocid(character_ocid, date)


def get_character_hexamatrix_stat(
    character_name: str,
    date: datetime = yesterday(),
) -> HexaMatrixStat:
    """
    HEXA 매트릭스에 설정한 HEXA 스탯 정보를 조회합니다.
    Fetches the HEXA stat information set in the HEXA matrix.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterHexaMatrixStat: 캐릭터의 HEXA 매트릭스 스탯 정보.
                                 The HEXA matrix stat information of the character.
    """

    character_ocid = get_character_id(character_name)
    return get_character_hexamatrix_stat_by_ocid(character_ocid, date)


def get_character_dojang_record(
    character_name: str,
    date: datetime = yesterday(),
) -> CharacterDojang:
    """
    캐릭터 무릉도장 최고 기록 정보를 조회합니다.
    Fetches the highest record information of the character's Dojang.

    Args:
        character_name : 캐릭터의 이름.
                         The name of the character.
        date : 조회 기준일 (KST).
                         Reference date for the query (KST).

    Returns:
        CharacterDojang: 캐릭터의 무릉도장 최고 기록 정보.
                         The highest record information of the character's Dojang.
    """

    character_ocid = get_character_id(character_name)
    return get_character_dojang_record_by_ocid(character_ocid, date)
