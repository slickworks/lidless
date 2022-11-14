import pytest
from tests.base import SRC_DIR, CONFIG_FILE, CACHE_DIR, DEST_DIR
from lidless.utils import join_paths
from lidless import Controller, Remote, LidlessConfigError


class TestBase:
    def setup_method(self) -> None:
        self.roots = {}
        self.default_key = "default"
        self.default_dest = DEST_DIR
        self.remotes = {self.default_key: {"tool": "rsync", "dest": self.default_dest}}

    def get_config(self) -> dict:
        return {
            "roots": self.roots,
            "remotes": self.remotes,
        }

    def get_controller(self) -> Controller:
        config = self.get_config()
        return Controller(CONFIG_FILE, CACHE_DIR, config)

    def get_remote(self, key="default") -> Remote:
        controller = self.get_controller()
        return controller.get_remote(key)

    def get_nodes(self, key="default"):
        return self.get_remote(key).nodes


class TestParsing(TestBase):
    def test_remote_names_valid(self):
        pass


class TestPathCollection(TestBase):
    def test_no_roots_yields_no_roots(self):
        self.roots = {}
        assert not self.get_nodes()

    def test_roots_without_slash_not_collected(self):
        self.roots = {
            "a": {"default": {}},
        }
        assert not self.get_nodes()

    def test_roots_which_dont_include_remote_are_not_collected(self):
        self.roots = {
            "/a": {"default": False},
            "/b": {"other": {}},
            "/c": {},
        }
        assert not self.get_nodes()

    def test_roots_collected_if_remote_true(self):
        self.roots = {
            "/a": {"default": True},
        }
        node, = self.get_nodes()
        assert node.path == "/a"

    def test_roots_collected_if_remote_empty(self):
        self.roots = {
            "/a": {"default": {}}
        }
        node, = self.get_nodes()
        assert node.path == "/a"

    def test_roots_collected_if_remote_has_others(self):
        self.roots = {
            "/a": {
                "default": {},
                "other": {},
            }
        }
        node, = self.get_nodes()
        assert node.path == "/a"

    def test_nested_nodes_collected_correctly_under_parent(self):
        self.roots = {
            "/a": {
                "default": {},
                "/nested": {
                    "default": {},
                }
            }
        }
        node1, node2 = self.get_nodes()
        assert node1.path == "/a"
        assert node2.path == "/a/nested"

    def test_nested_nodes_collected_even_if_parent_isnt(self):
        self.roots = {
            "/a": {
                "/nested": {
                    "default": {},
                }
            }
        }
        node, = self.get_nodes()
        assert node.path == "/a/nested"

    def test_nested_node_not_collected_under_invalid_parent(self):
        self.roots = {
            "a": {
                "/nested": {
                    "default": {},
                }
            }
        }
        assert not self.get_nodes()


class TestDestinations(TestBase):
    def test_duplicate_destinations_not_allowed(self):
        self.roots = {
            "/a": {"default": {}},
            "/b": {"default": {}},
        }
        with pytest.raises(LidlessConfigError):
            self.get_nodes()

    def test_single_root_can_forego_dest(self):
        self.roots = {
            "/a": {"default": {}},
        }
        node, = self.get_nodes()
        assert node.dest == self.default_dest

    def test_nested_node_gets_correct_dest(self):
        self.roots = {
            "/a": {
                "/nested": {
                    "default": {},
                }
            },
        }
        node, = self.get_nodes()
        assert node.dest == join_paths(self.default_dest, "/nested")

    def test_setting_dest_in_node(self):
        self.roots = {
            "/a": {
                "dest": "foo",
                "default": {},
                "/nested": {
                    "default": {},
                }
            },
        }
        node1, node2 = self.get_nodes()
        assert node1.dest == join_paths(self.default_dest, "foo")
        assert node2.dest == join_paths(self.default_dest, "foo", "/nested")
