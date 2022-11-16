from lidless.exceptions import LidlessConfigError
from lidless.models import Node
from lidless.utils import join_paths, find_duplicates


class NodeCollector:

    def __init__(self, roots, base_dest='', collect_tags=None, default_tags=None):
        self.collect_tags = collect_tags
        self.default_tags = default_tags
        self.roots = roots
        self.base_dest = base_dest
        self.collected_nodes = []

    def get_nodes(self):
        self.collected_nodes = []
        self._collect(self.roots, self.base_dest)
        duplicate_dests = find_duplicates([node.dest for node in self.collected_nodes])
        if duplicate_dests:
            raise LidlessConfigError("\n".join(duplicate_dests))
        return self.collected_nodes

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
                    self.collected_nodes.append(
                        self._get_node(
                            node_path, base_dest, base_path, node_data
                        )
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


def collect_nodes(roots, base_dest, target_tags, default_tags):
    c = NodeCollector(roots, base_dest, target_tags, default_tags)
    return c.get_nodes()