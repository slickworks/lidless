import pytest


@pytest.fixture
def fileset1():
    return """
    foo
    foo/bar.txt
    foo/foo.txt
    """

@pytest.fixture
def fileset2():
    return """
    foo
    foo/foo.txt
    bar
    """