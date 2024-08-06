from packaging.version import Version

import cartesia.version as version
from cartesia.utils.deprecated import _DEPRECATED_FUNCTION_STATS


def test_deprecated_to_remove_by_version():
    """
    Test that all deprecated functions that are listed to be
    removed by the current version are removed.
    """
    versions_to_remove = [x["vremove"] for x in _DEPRECATED_FUNCTION_STATS]
    versions_to_remove = [Version(x) for x in versions_to_remove if x is not None]

    curr_version = Version(version.__version__)

    assert all(v > curr_version for v in versions_to_remove)
    
# This test is taken from the following source:
# https://github.com/ad12/meddlr/blob/main/tests/utils/test_deprecated.py
