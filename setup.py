"""
https://cx-freeze.readthedocs.io/en/latest/
"""
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {"packages": [], "excludes": []}

base = "console"

executables = [Executable("lidless/__main__.py", base=base, target_name="lidless")]

setup(
    name="lidless",
    version="1.0",
    description="",
    options={"build_exe": build_options},
    executables=executables,
)
