from .base import BaseWithTarget


class TestExclude(BaseWithTarget):
    def test_nested_dirs_are_excluded(self):
        self.roots = {"/a": {"tags": [self.target_tag], "/nested": {}}}
        (node,) = self.get_nodes(self.target_key)
        assert node.exclude == ["/nested"]

    def test_excplicit_exclude_are_excluded(self):
        self.roots = {"/a": {"tags": [self.target_tag], "exclude": ["foo"]}}
        (node,) = self.get_nodes(self.target_key)
        assert node.exclude == ["foo"]

    def test_exclude_are_combined_and_sorted_with_no_dupes(self):
        self.roots = {
            "/a": {
                "tags": [self.target_tag],
                "exclude": ["/foo", "/bar"],
                "/nested": {},
                "/bar": {},
            }
        }
        (node,) = self.get_nodes(self.target_key)
        assert node.exclude == ["/bar", "/foo", "/nested"]
