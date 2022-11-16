from .base import TestBase


class TestParsing(TestBase):

    def test_config_has_expected_entries(self):
        pass
        #test they are of correct types

    def test_target_names_are_valid(self):
        self.targets["!foo"] = {}
        self.get_controller()

    def test_targets_have_required_keys(self):
        pass

    def test_roots_start_with_slashes(self):
        pass