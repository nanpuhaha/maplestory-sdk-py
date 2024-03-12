import pytest

from maplestory.utils.params import every_element_contains, every_element_not_contains


class TestEveryElementContains:

    # Returns True if every element in the list contains the given key
    def test_returns_true_if_every_element_contains_key(self):
        lis = ["apple", "banana", "orange"]
        key = "a"
        result = every_element_contains(lis, key)
        assert result is True

    # Raises a TypeError if the input list contains elements that are not strings
    def test_raises_type_error_if_list_contains_non_string_elements(self):
        lis = ["apple", 123, "orange"]
        key = "a"
        with pytest.raises(TypeError):
            every_element_contains(lis, key)

    # Returns False if the list is empty
    def test_returns_true_if_list_is_empty(self):
        lis = []
        key = "a"
        result = every_element_contains(lis, key)
        assert result is False

    # Returns False if the list contains only None values and the key is not None
    def test_returns_false_if_list_contains_only_none_values_and_key_is_not_none(self):
        lis = [None, None, None]
        key = "a"
        result = every_element_contains(lis, key)
        assert result is False

    # Returns False if the key is not in any of the elements in the list
    def test_returns_false_if_key_not_in_elements(self):
        lis = ["apple", "banana", "orange"]
        key = "m"
        result = every_element_contains(lis, key)
        assert result is False

    # Raises a TypeError if the input key is not a string
    def test_raises_type_error_if_key_not_string(self):
        lis = ["apple", "banana", "orange"]
        key = 123
        with pytest.raises(TypeError):
            every_element_contains(lis, key)

    # Returns False if the input list is None
    def test_returns_false_if_list_is_none(self):
        lis = None
        key = "apple"
        result = every_element_contains(lis, key)
        assert result is False


class TestEveryElementNotContains:

    # Returns True when the list is empty.
    def test_empty_list_returns_true(self):
        lis = []
        key = "abc"
        assert every_element_not_contains(lis, key) is True

    # Returns True when none of the elements in the list contain the key.
    def test_none_of_elements_contain_key(self):
        lis = ["apple", "banana", "orange"]
        key = "fruit"
        assert every_element_not_contains(lis, key) is True

    # Returns False when all elements in the list contain the key.
    def test_all_elements_contain_key(self):
        lis = ["apple", "banana", "orange"]
        key = "a"
        assert every_element_not_contains(lis, key) is False

    # Returns False when the key is an empty string and some elements in the list are also empty strings.
    def test_empty_key_and_empty_elements_returns_false(self):
        lis = ["", "abc", "", "def"]
        key = ""
        assert every_element_not_contains(lis, key) is False

    # Returns False when the key is an empty string and all elements in the list are non-empty strings.
    def test_empty_key_and_non_empty_elements_returns_true(self):
        lis = ["abc", "def", "ghi"]
        key = ""
        assert every_element_not_contains(lis, key) is False

    # Returns True when the list contains only one element and that element is None.
    def test_list_with_single_none_element_returns_true(self):
        lis = [None]
        key = "abc"
        assert every_element_not_contains(lis, key) is True

    # Returns True when the list contains only one element and that element does not contain the key.
    def test_list_with_single_element_not_containing_key_returns_true(self):
        lis = ["def"]
        key = "abc"
        assert every_element_not_contains(lis, key) is True

    # Returns False when the list contains only one element and that element contains the key.
    def test_list_with_single_element_containing_key_returns_false(self):
        lis = ["abcdef"]
        key = "abc"
        assert every_element_not_contains(lis, key) is False
