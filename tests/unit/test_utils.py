from lidless.utils import get_src_and_dest, join_paths, map_to_pairs


def test_join_paths():
    assert join_paths("/foo", "bar") == "/foo/bar"
    assert join_paths("/foo/", "bar") == "/foo/bar"
    assert join_paths("/foo/", "/bar") == "/foo/bar"
    assert join_paths("/foo", "/bar") == "/foo/bar"
    assert join_paths("/foo", "/bar/") == "/foo/bar"

    assert join_paths("/foo", "/bar", add_end=True) == "/foo/bar/"
    assert join_paths("/foo", "/bar", add_start=False) == "foo/bar"

def test_get_src_and_dest():
    maps = {
        "/foo": "/mnt/ext/foo"
    }
    path = "/foo/bar"
    src, dest = get_src_and_dest(path, maps, False)
    assert src == path + "/"
    assert dest == "/mnt/ext/foo/bar/"


def test_map_to_pairs():
    maps = {
        "/foo": "/mnt/ext/foo",
        "/foo/bar": "/mnt/ext/foo/bar"
    }
    pairs = map_to_pairs(maps, False)
    assert pairs == [
        ("/foo/bar", "/mnt/ext/foo/bar"),
        ("/foo", "/mnt/ext/foo")
    ]

    pairs = map_to_pairs(maps, True)
    assert pairs == [
        ("/mnt/ext/foo/bar", "/foo/bar"),
        ("/mnt/ext/foo", "/foo")
    ]
