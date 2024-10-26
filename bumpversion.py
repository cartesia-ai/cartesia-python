"""Bump the version of the package.

Usage: bumpversion.py <version>

<version> must be in the format of <major>.<minor>.<patch>[-<prelabel><preversion>]
"""

import re
import tomlkit
import sys
from cartesia.version import __version__

VERSION_REGEX = r"""(?x)
    (?P<major>0|[1-9]\d*)\.
    (?P<minor>0|[1-9]\d*)\.
    (?P<patch>0|[1-9]\d*)
    (?:
        -                             # dash separator for pre-release section
        (?P<prelabel>[a-zA-Z-]+)         # pre-release label
        (?P<preversion>0|[1-9]\d*)        # pre-release version number
    )?                                # pre-release section is optional
"""  # Source: https://github.com/callowayproject/bump-my-version


def main(version: str):
    assert re.match(VERSION_REGEX, version), "Invalid version format"

    with open("pyproject.toml", "r") as f:
        pyproject = tomlkit.load(f)

    pyproject["project"]["version"] = version

    with open("pyproject.toml", "w") as f:
        tomlkit.dump(pyproject, f)

    with open("cartesia/version.py", "w") as f:
        f.write(f'__version__ = "{version}"\n')


if __name__ == "__main__":
    main(sys.argv[1])
