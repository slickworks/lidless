import os
import math
from lidless.exceptions import LidlessConfigError

def join_paths(*paths, add_start=True, add_end=False, separator="/"):
    """
    Joins paths with single instance of separator regardless of whether the
    paths start or end with sep. Optionally adds separator to start and/or end.
    """
    mash = separator.join(paths)
    chunks = mash.split(separator)
    joined = separator.join(s for s in chunks if len(s))
    if add_start:
        joined = separator + joined
    if add_end:
        joined = joined + separator
    return joined


def create_file(path, contents):
    create_dir(os.path.dirname(path))
    with open(path, "w") as fp:
        fp.write(contents)


def create_dir(path):
    os.makedirs(path, exist_ok=True)


def find_duplicates(items):
    seen = set()
    dupes = []

    for x in items:
        if x in seen:
            dupes.append(x)
        else:
            seen.add(x)

    return dupes


def get_path_leaves(paths):
    unique = set()
    remove = set()

    for path in paths:
        if os.path.isdir(path):
            unique.add(path)

    for path in unique:
        for other in unique:
            if other != path and other.startswith(path):
                remove.add(path)

    for path in remove:
        unique.remove(path)

    return sorted(unique)


def get_src_and_dest(path, maps, invert):
    pairs = map_to_pairs(maps, invert)
    dest = substitute_path(path, pairs)
    dest = trailing_sep(dest)
    path = trailing_sep(path)
    if invert:
        return dest, path
    return path, dest


def trailing_sep(path, sep="/"):
    return path.rstrip(sep) + sep


def substitute_path(path, pairs):
    for a, b in pairs:
        if path.startswith(a):
            path = path[len(a) :]
            return join_paths(b, path)
    # TODO: make a more specific exception and handle upstream, also test
    raise LidlessConfigError(f"Path not included in maps: {path}")


def map_to_pairs(maps, invert):
    pairs = []
    for k, v in maps.items():
        if invert:
            pair = v, k
        else:
            pair = k, v
        pairs.append(pair)
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    return pairs


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s}{size_name[i]}"
