from os.path import expanduser, dirname, join, exists
import json

from lidless.exceptions import LidlessConfigError
from lidless.models import Node, Remote
from lidless.tools import get_tool
from lidless.utils import join_paths, find_duplicates


BASE = dirname(dirname(dirname(__file__)))  # TODO: change!
DEFAULT_CONFIG_FILE = join(BASE, "backup.config.json")
DEFAULT_CACHE_DIR = join(BASE, ".cache")


class Controller:
    config_file: str
    cache_dir: str

    def __init__(
        self, config_file=DEFAULT_CONFIG_FILE, cache_dir=DEFAULT_CACHE_DIR, data=None
    ) -> None:
        self.config_file = expanduser(config_file)
        self.cache_dir = expanduser(cache_dir)
        self.__data: dict = data or {}

    @property
    def data(self) -> dict:
        self._load()
        return self.__data

    def _load(self):
        if not len(self.__data):
            if exists(self.config_file):
                with open(self.config_file) as fp:
                    self.__data = json.load(fp)
            else:
                self.__data = {"nodes": {}, "exclude": [], "remotes": {}}

    def get_remote(self, remote_key):
        config_remotes = self.data["remotes"]
        remote_data = config_remotes[remote_key]
        base_dest = remote_data.get("dest", "")
        return Remote(
            config=self,
            name=remote_key,
            tool=get_tool(remote_key, remote_data),
            nodes=self._collect_nodes(remote_key, base_dest),
        )

    def _collect_nodes(self, remote_key, base_dest):
        # TODO: push out to node collector class
        node_list = []
        self._get_nodes(node_list, remote_key, base_dest)
        duplicate_dests = find_duplicates([node.dest for node in node_list])
        if duplicate_dests:
            raise LidlessConfigError("\n".join(duplicate_dests))
        return node_list

    def _get_nodes(
        self,
        collected_nodes,
        remote_key,
        base_dest,
        base_path=None,
        parent_path="",
        node=None,
    ):
        """
        Recursive function which traverses down tree of nodes.


            - allow dest override at node level, or in remote config
            - collect exclude lists (extend, cat, override)
            - add special tests for root nodes:
                must have a dest, which must be unique
                (or should all collected dests be unique?)

        @remote_key - stays constant, used for collecting.

        """
        # consider bringing back collected_nodes is None
        if node is None:
            node = self.data["roots"]
        for path, node_data in node.items():
            if path.startswith("/"):
                base_path = base_path or path
                node_path = join_paths(parent_path, path)
                node_remotes = self._get_node_remotes(node_data)
                if remote_key in node_remotes:
                    remote_data = node_remotes[remote_key]
                    if remote_data or remote_data == {}:
                        # dest = remote_data.get("dest", "")
                        # dest = join_paths(parent_dest, dest)
                        collected_nodes.append(
                            self._get_node(
                                node_path, base_dest, base_path, remote_data, node_data
                            )
                        )
                        print(node_path, remote_data, len(collected_nodes))
                self._get_nodes(
                    collected_nodes,
                    remote_key,
                    base_dest,
                    base_path,
                    node_path,
                    node_data,
                )

    def _get_node_remotes(self, node_data):
        return {k: v for k, v in node_data.items() if not k.startswith("/")}

    def _get_node(self, node_path, base_dest, base_path, remote_data, node_data):
        # print('base_path:', base_path)
        # print('base_dest:', base_dest)
        # print('node_path:', node_path)
        # print('dest:', self._get_dest(base_dest, node_path, base_path))
        # print('-----------')
        return Node(
            config=self,
            path=node_path,
            dest=self._get_dest(base_dest, node_path, base_path),
            exclude=[],
        )

    def _get_dest(self, base_dest, node_path, base_path):
        cut = len(base_path)
        rel = node_path[cut:]
        return join_paths(base_dest, rel).rstrip("/")

    # def get_nodes(self):
    #     nodes = []
    #     for node_path, node_data in self.data["nodes"].items():
    #         repos = []
    #         for repo_path, repo_data in node_data.get("repos", {}):
    #             repos.append(Repo(
    #                 config=self,
    #                 path=repo_path,
    #                 remote=repo_data.get("remote", ""),
    #                 save=repo_data.get("save", []),
    #             ))
    #         nodes.append(Node(
    #             config=self,
    #             path=node_path,
    #             exclude=node_data.get("exclude", []),
    #             repos=repos,
    #         ))
    #     return nodes

    def get_exclude_file(self, path, exclude):
        pass

    def _save(self):
        with open(self.config_file, "w") as fp:
            json.dump(self.__data, fp, indent=4)

    def add_remote(self, name, cmd):
        self.data["remotes"][name] = {"cmd": cmd}
        self._save()

    def add_node(self, path):
        pass

    def add_repo(self, path):
        pass
