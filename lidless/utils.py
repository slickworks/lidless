import os


def join_paths(*paths):
    """Safely join paths which may omit slashes."""
    first = paths[0]
    start = "/" if first.startswith("/") else ""
    return start + "/".join(path.strip("/") for path in paths)


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
