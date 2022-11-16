import pytest
from lidless.utils import join_paths
from lidless import LidlessConfigError
from .base import BaseWithTarget


class TestDestinations(BaseWithTarget):
    def test_duplicate_destinations_not_allowed(self):
        self.roots = {
            "/a": {"tags": [self.target_tag]},
            "/b": {"tags": [self.target_tag]},
        }
        with pytest.raises(LidlessConfigError):
            self.get_nodes(self.target_key)

    def test_single_root_can_forego_dest(self):
        self.roots = {
            "/a": {"tags": [self.target_tag]},
        }
        node, = self.get_nodes(self.target_key)
        assert node.dest == self.default_dest

    def test_nested_node_gets_correct_dest(self):
        self.roots = {
            "/a": {
                "/nested": {
                    "tags": [self.target_tag]
                }
            },
        }
        node, = self.get_nodes(self.target_key)
        assert node.dest == join_paths(self.default_dest, "/nested")

    def test_setting_dest_in_root(self):
        self.roots = {
            "/a": {
                "dest": "foo",
                "tags": [self.target_tag],
                "/nested": {
                    "tags": [self.target_tag]
                }
            },
        }
        node1, node2 = self.get_nodes(self.target_key)
        assert node1.dest == join_paths(self.default_dest, "foo")
        assert node2.dest == join_paths(self.default_dest, "foo", "/nested")

    def test_setting_dest_in_nested_node(self):
        self.roots = {
            "/a": {
                "dest": "foo",
                "tags": [self.target_tag],
                "/nested": {
                    "dest": "bar",
                    "tags": [self.target_tag]
                }
            },
        }
        node1, node2 = self.get_nodes(self.target_key)
        assert node1.dest == join_paths(self.default_dest, "foo")
        # Is this what we want?
        assert node2.dest == join_paths(self.default_dest, "foo/bar", "/nested")
