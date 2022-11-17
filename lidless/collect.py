from collections import defaultdict
from lidless.exceptions import DuplicateDestinationsError
from lidless.models import Node
from lidless.utils import join_paths


class NodeCollector:
    def __init__(self, roots, base_dest="", collect_tags=None, default_tags=None):
        self.collect_tags = collect_tags
        self.default_tags = default_tags
        self.roots = roots
        self.base_dest = base_dest
        self._nodes = []

    def get_nodes(self):
        self._nodes = []
        self._collect(self.roots, self.base_dest)
        self._find_duplicate_destinations()
        return self._nodes

    def _collect(
        self,
        node,
        base_dest,
        base_path=None,
        parent_path="",
    ):
        """
        Recursive function which walks down tree of nodes.
        """
        for path, node_data in node.items():
            if path.startswith("/"):
                base_path = base_path or path
                node_path = join_paths(parent_path, path)
                if self._should_include_node(node_data):
                    node_dest = node_data.get("dest")
                    if node_dest:
                        base_dest = join_paths(base_dest, node_dest)
                    self._nodes.append(
                        self._get_node(node_path, base_dest, base_path, node_data)
                    )
                self._collect(
                    node_data,
                    base_dest,
                    base_path,
                    node_path,
                )

    def _should_include_node(self, node_data):
        if not self.collect_tags:
            return True
        node_tags = self._get_node_tags(node_data)
        for tag in self.collect_tags:
            if tag in node_tags:
                return True
        return False

    def _get_node_tags(self, node_data):
        return node_data.get("tags", self.default_tags or [])

    def _get_node(self, node_path, base_dest, base_path, node_data):

        return Node(
            config=self,
            path=node_path,
            dest=self._get_dest(base_dest, node_path, base_path),
            exclude=self._get_exclude(node_data),
        )

    def _get_exclude(self, node_data):
        nested = [entry for entry in node_data.keys() if entry.startswith("/")]
        exclude = node_data.get("exclude", [])
        unique = set(nested + exclude)
        combined = list(unique)
        combined.sort()
        return combined

    def _get_dest(self, base_dest, node_path, base_path):
        cut = len(base_path)
        rel = node_path[cut:]
        return join_paths(base_dest, rel).rstrip("/")

    def _find_duplicate_destinations(self):
        """
        Raises an error if nodes are found with duplicate destinations.
        """
        node_dests = defaultdict(list)
        for node in self._nodes:
            node_dests[node.dest].append(node.path)

        duplicates = {}
        for dest, paths in node_dests.items():
            if len(paths) > 1:
                duplicates[dest] = paths

        if duplicates:
            raise DuplicateDestinationsError(duplicates)


def collect_nodes(roots, base_dest, target_tags, default_tags):
    c = NodeCollector(roots, base_dest, target_tags, default_tags)
    return c.get_nodes()
