# Codium

import pytest

from maplestory.apis.guild import get_guild_id
from maplestory.error import APIError, APIErrorCode, ErrorMessage


class TestFromCode:

    # Should return the corresponding APIErrorCode enum value when given a valid code string
    def test_valid_code_string(self):
        code = "OPENAPI00001"
        result = APIErrorCode.from_code(code)
        assert result == APIErrorCode.OPENAPI00001

    # Should be able to handle all valid APIErrorCode enum values
    def test_all_valid_enum_values(self):
        for code in APIErrorCode:
            result = APIErrorCode.from_code(code.name)
            assert result == code

    # Should be case-sensitive when matching code strings to enum values
    def test_case_sensitive_matching(self):
        code = "openapi00001"
        with pytest.raises(KeyError):
            APIErrorCode.from_code(code)

    # Should raise a KeyError when given an invalid code string that doesn't match any APIErrorCode enum value
    def test_invalid_code_string(self):
        code = "INVALIDCODE"
        with pytest.raises(KeyError):
            APIErrorCode.from_code(code)

    # Should raise a TypeError when given a code parameter that is not a string
    def test_non_string_code_parameter(self):
        code = 12345
        with pytest.raises(KeyError):
            APIErrorCode.from_code(code)

    # Should raise a ValueError when given an empty string as the code parameter
    def test_empty_string_code_parameter(self):
        code = ""
        with pytest.raises(KeyError):
            APIErrorCode.from_code(code)


# ------------------------------------------------

# Sourcery

# Parametrized test for happy path scenarios
# @pytest.mark.parametrize("code, expected_enum", [
#     pytest.param("서버 내부 오류", APIErrorCode.OPENAPI00001, id="happy_path_error_1"),
#     pytest.param("권한이 없는 경우", APIErrorCode.OPENAPI00002, id="happy_path_error_2"),
#     pytest.param("유효하지 않은 식별자", APIErrorCode.OPENAPI00003, id="happy_path_error_3"),
#     pytest.param("파라미터 누락 또는 유효하지 않음", APIErrorCode.OPENAPI00004, id="happy_path_error_4"),
#     pytest.param("유효하지 않은 API KEY", APIErrorCode.OPENAPI00005, id="happy_path_error_5"),
#     pytest.param("유효하지 않은 게임 또는 API PATH", APIErrorCode.OPENAPI00006, id="happy_path_error_6"),
#     pytest.param("API 호출량 초과", APIErrorCode.OPENAPI00007, id="happy_path_error_7"),
#     pytest.param("데이터 준비 중", APIErrorCode.OPENAPI00009, id="happy_path_error_9"),
#     # Add more test cases for different error codes
# ])
# def test_from_code_happy_path(value, expected_enum):
#     # Act
#     result = APIErrorCode(value=value)

#     # Assert
#     assert result == expected_enum, f"Expected {expected_enum} for code {value}"

# Parametrized test for edge cases
# Assuming there are no specific edge cases for this Enum conversion as it's straightforward


# Parametrized test for error cases
@pytest.mark.parametrize(
    "code, expected_exception",
    [
        pytest.param("", KeyError, id="error_case_empty_string"),
        pytest.param("UNKNOWN_CODE", KeyError, id="error_case_unknown_code"),
        pytest.param(None, KeyError, id="error_case_none"),
        pytest.param(123, KeyError, id="error_case_numeric_code"),
        # Add more test cases for different invalid inputs
    ],
)
def test_from_code_error_cases(code, expected_exception):
    # Act & Assert
    with pytest.raises(expected_exception):
        _ = APIErrorCode.from_code(code)


# ------------------------------------------------
# Chat


def test_api_error_code():
    assert APIErrorCode.from_code("OPENAPI00001") == APIErrorCode.OPENAPI00001
    assert APIErrorCode.from_code("OPENAPI00002") == APIErrorCode.OPENAPI00002
    assert APIErrorCode.from_code("OPENAPI00003") == APIErrorCode.OPENAPI00003
    assert APIErrorCode.from_code("OPENAPI00004") == APIErrorCode.OPENAPI00004
    assert APIErrorCode.from_code("OPENAPI00005") == APIErrorCode.OPENAPI00005
    assert APIErrorCode.from_code("OPENAPI00006") == APIErrorCode.OPENAPI00006
    assert APIErrorCode.from_code("OPENAPI00007") == APIErrorCode.OPENAPI00007
    assert APIErrorCode.from_code("OPENAPI00009") == APIErrorCode.OPENAPI00009


def test_error_message():
    error = ErrorMessage(name="OPENAPI00004", message="Please input valid parameter")
    assert error.code == "OPENAPI00004"
    assert error.message == "Please input valid parameter"


# RuntimeError: The request instance has not been set on this response.
def test_api_error():
    with pytest.raises(APIError) as api_error:
        _ = get_guild_id("없는길드명", "없는서버명")
        assert api_error.code == "OPENAPI00004"
        assert api_error.message == "Please input valid parameter"
        assert api_error.status == 400
        assert api_error.description == APIErrorCode.OPENAPI00004.value
