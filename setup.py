#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev
import shutil
import subprocess
import sys
from distutils.util import convert_path
from shutil import rmtree

from setuptools import Command, find_packages, setup

PACKAGE_DIR = "cartesia"
main_ns = {}
ver_path = convert_path(os.path.join(PACKAGE_DIR, "version.py"))
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


# Package meta-data.
NAME = "cartesia"
DESCRIPTION = "The official Python library for the Cartesia API."
URL = ""
EMAIL = "support@cartesia.ai"
AUTHOR = "Cartesia, Inc."
REQUIRES_PYTHON = ">=3.8.0"
VERSION = main_ns["__version__"]


# What packages are required for this module to be executed?
def get_requirements(path):
    with open(path, "r") as f:
        out = f.read().splitlines()

    out = [line.strip() for line in out]
    return out


REQUIRED = get_requirements("requirements.txt")
REQUIRED_DEV = get_requirements("requirements-dev.txt")

# What packages are optional?
EXTRAS = {
    "dev": REQUIRED_DEV,
}
EXTRAS["all"] = [pkg for group in EXTRAS.values() for pkg in group]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = [("skip-upload", "u", "skip git tagging and pypi upload")]
    boolean_options = ["skip-upload"]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        self.skip_upload = False

    def finalize_options(self):
        self.skip_upload = bool(self.skip_upload)

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
            rmtree(os.path.join(here, "build"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        if self.skip_upload:
            self.status("Skipping git tagging and pypi upload")
            sys.exit()

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


class BumpVersionCommand(Command):
    """
    To use: python setup.py bumpversion -v <version>

    This command will push the new version directly and tag it.

    Usage:
        python setup.py bumpversion --version=1.0.1
    """

    description = "Installs the foo."
    user_options = [
        ("version=", "v", "the new version number"),
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        self.version = None
        self.base_branch = None
        self.version_branch = None
        self.updated_files = [
            "cartesia/version.py",
        ]

    def finalize_options(self):
        # This package cannot be imported at top level because it
        # is not recognized by Github Actions.
        from packaging import version

        if self.version is None:
            raise ValueError("Please specify a version number.")

        current_version = about["__version__"]
        if not version.Version(self.version) > version.Version(current_version):
            raise ValueError(
                f"New version ({self.version}) must be greater than "
                f"current version ({current_version})."
            )

    def _undo(self):
        os.system(f"git restore --staged {' '.join(self.updated_files)}")
        os.system(f"git checkout -- {' '.join(self.updated_files)}")

        # Return to the original branch
        os.system(f"git checkout {self.base_branch}")
        os.system(f"git branch -D {self.version_branch}")

    def run(self):
        current_version = about["__version__"]

        self.status("Checking current branch is 'main'")
        self.base_branch = current_branch = get_git_branch()
        if current_branch != "main":
            raise RuntimeError(
                "You can only bump the version from the 'main' branch. "
                "You are currently on the '{}' branch.".format(current_branch)
            )

        self.status("Pulling latest changes from origin")
        err_code = os.system("git pull")
        if err_code != 0:
            raise RuntimeError("Failed to pull from origin.")

        self.status("Checking working directory is clean")
        err_code = os.system("git diff --exit-code")
        err_code += os.system("git diff --cached --exit-code")
        if err_code != 0:
            raise RuntimeError("Working directory is not clean.")

        # TODO: Add check to see if all tests are passing on main.

        # Checkout new branch
        self.version_branch = f"bumpversion/v{self.version}"
        self.status(f"Create branch '{self.version_branch}'")
        err_code = os.system(f"git checkout -b {self.version_branch}")
        if err_code != 0:
            raise RuntimeError("Failed to create branch.")

        # Change the version in __init__.py
        self.status(f"Updating version {current_version} -> {self.version}")
        update_version(self.version)
        # if current_version != self.version:
        #     self._undo()
        #     raise RuntimeError("Failed to update version.")

        self.status(f"Adding {', '.join(self.updated_files)} to git")
        err_code = os.system(f"git add {' '.join(self.updated_files)}")
        if err_code != 0:
            self._undo()
            raise RuntimeError("Failed to add files to git.")

        # Commit the file with a message '[bumpversion] v<version>'.
        self.status(f"Commit with message '[bumpversion] v{self.version}'")
        err_code = os.system("git commit -m '[bumpversion] v{}'".format(self.version))
        if err_code != 0:
            self._undo()
            raise RuntimeError("Failed to commit file to git.")

        # Push the commit to origin.
        self.status(f"Pushing commit to origin/{self.version_branch}")
        err_code = os.system(f"git push --force --set-upstream origin {self.version_branch}")
        if err_code != 0:
            # TODO: undo the commit automatically.
            self._undo()
            raise RuntimeError("Failed to push commit to origin.")

        os.system(f"git checkout {self.base_branch}")
        os.system(f"git branch -D {self.version_branch}")
        sys.exit()


def update_version(version):
    import json

    # Update python.
    init_py = [
        line if not line.startswith("__version__") else f'__version__ = "{version}"\n'
        for line in open(ver_path, "r").readlines()
    ]
    with open(ver_path, "w") as f:
        f.writelines(init_py)


def get_git_branch():
    """Return the name of the current branch."""
    proc = subprocess.Popen(["git branch"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if err is not None:
        raise RuntimeError(f"Error finding git branch: {err}")
    out = out.decode("utf-8").split("\n")
    current_branch = [line for line in out if line.startswith("*")][0]
    current_branch = current_branch.replace("*", "").strip()
    return current_branch


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=[PACKAGE_DIR],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand, "bumpversion": BumpVersionCommand},
)
