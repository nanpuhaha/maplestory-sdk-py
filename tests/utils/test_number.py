import pytest

from maplestory.utils.number import korean_format_number


class TestFormatNumberKorean:
    # The function returns '0' when given 0 as input.
    def test_returns_zero_when_given_zero(self):
        assert korean_format_number(0) == "0"

    # The function correctly formats numbers with up to 4 digits.
    def test_correctly_formats_numbers_with_up_to_four_digits(self):
        assert korean_format_number(1) == "1"
        assert korean_format_number(12) == "12"
        assert korean_format_number(123) == "123"
        assert korean_format_number(1234) == "1234"

    # The function correctly formats numbers with 5 digits.
    def test_correctly_formats_numbers_with_five_digits(self):
        assert korean_format_number(12345) == "1만 2345"

    # The function correctly formats the big integer value.
    def test_correctly_formats_big_integer_value(self):
        assert korean_format_number(27439263548400) == "27조 4392억 6354만 8400"

    # The function correctly formats the maximum integer value.
    def test_correctly_formats_maximum_integer_value(self):
        assert (
            korean_format_number(9223372036854775807)
            == "922경 3372조 368억 5477만 5807"
        )

    # The function correctly formats the minimum integer value.
    def test_correctly_formats_minimum_integer_value(self):
        assert korean_format_number(-9223372036854775808) == "0"

    # The function raises a TypeError when given a non-integer input.
    def test_raises_type_error_when_given_non_integer_input(self):
        with pytest.raises(TypeError):
            korean_format_number("123")
