import pytest

from maplestory.services.character import CharacterExperience


class TestCharacterExperience:
    # Verify if the experience required for the next level is correctly retrieved.
    def test_required_exp_for_next_level(self):
        assert CharacterExperience.from_level(50).required_exp_for_next_level == 110870

    # Confirm retrieval of required experience for a given level matches expected value.
    def test_retrieve_required_exp(self):
        assert CharacterExperience.from_level(50).required == 110870

    # Check if cumulative experience up to a specific level is accurately calculated.
    def test_retrieve_cumulative_exp(self):
        assert CharacterExperience.from_level(50).cumulative == 1126986

    # Validate level determination from a given cumulative experience amount.
    def test_retrieve_level_from_cumulative_exp(self):
        assert CharacterExperience.from_level(50) == CharacterExperience.LEVEL_50

    # Ensure non-integer level input is correctly handled and interpreted.
    def test_handle_non_integer_level(self):
        assert CharacterExperience.from_level("50") == CharacterExperience.LEVEL_50

    # Test retrieval of experience required to reach the maximum level.
    def test_required_exp_for_max_level(self):
        assert CharacterExperience.LEVEL_300.required_exp_for_max_level == 0

    # Ensure that querying 'required_exp_for_max_level' at levels other than the maximum returns a logical value.
    def test_required_exp_for_max_level_for_non_max_level(self):
        assert (
            CharacterExperience.from_level(50).required_exp_for_max_level
            == 8514022614596349
        )

    # Confirm appropriate error handling when a level above the maximum is queried.
    def test_from_level_greater_than_max_level(self):
        with pytest.raises(KeyError):
            CharacterExperience.from_level(301)

    # Verify error handling for negative level inputs.
    def test_handle_negative_level(self):
        with pytest.raises(KeyError):
            CharacterExperience.from_level(-1)
