from .base import BaseWithTarget


class TestPathCollection(BaseWithTarget):
    def test_no_roots_yields_no_roots(self):
        self.roots = {}
        assert not self.get_nodes(self.target_key)

    def test_roots_without_slash_not_collected(self):
        self.roots = {
            "a": {},
        }
        assert not self.get_nodes(self.target_key)

    def test_only_roots_with_tag_are_collected(self):
        self.roots = {
            "/a": {"dest": "a", "tags": ["other"]},
            "/b": {"dest": "b", "tags": []},
            "/c": {"dest": "c", "tags": [self.target_tag, "other"]},
            "/d": {"dest": "d", "tags": [self.target_tag]},
            "/e": {},
        }
        node1, node2 = self.get_nodes(self.target_key)
        assert node1.path == "/c"
        assert node2.path == "/d"

    def test_nested_nodes_collected(self):
        self.roots = {
            "/a": {
                "tags": [self.target_tag],
                "/nested": {
                    "tags": [self.target_tag],
                },
            }
        }
        node1, node2 = self.get_nodes(self.target_key)
        assert node1.path == "/a"
        assert node2.path == "/a/nested"

    def test_nested_nodes_collected_when_parent_isnt(self):
        self.roots = {
            "/a": {
                "/nested": {
                    "tags": [self.target_tag],
                }
            }
        }
        (node,) = self.get_nodes(self.target_key)
        assert node.path == "/a/nested"

    def test_nested_node_not_collected_under_invalid_parent(self):
        self.roots = {
            "a": {
                "/nested": {
                    "tags": [self.target_tag],
                }
            }
        }
        assert not self.get_nodes(self.target_key)

    def test_tags_are_not_inherited(self):
        self.roots = {
            "/a": {
                "/nested": {
                    "tags": [self.target_tag],
                    "/sub1": {"tags": []},
                    "/sub2": {},
                }
            }
        }
        (node,) = self.get_nodes(self.target_key)
        assert node.path == "/a/nested"


class TestPathCollectionWithDefaultTags(BaseWithTarget):
    def setup_method(self):
        super().setup_method()
        self.settings = {"default_tags": [self.target_tag]}

    # def test_only_roots_with_tag_are_collected(self):
    #     self.roots = {
    #         "/a": {"dest": "a", "tags": ["other"]},
    #         "/b": {"dest": "b", "tags": []},
    #         "/c": {"dest": "c", "tags": [self.target_tag, "other"]},
    #         "/d": {"dest": "d", "tags": [self.target_tag]},
    #         "/e": {},
    #     }
    #     node1, node2, node3 = self.get_nodes(self.target_key)
    #     assert node1.path == "/c"
    #     assert node2.path == "/d"
    #     assert node2.path == "/e"
