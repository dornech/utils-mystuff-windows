# utilities

"""
Package with various utilities depending on windows platform i. e. windows handling

Set of submodules contains:

- submodule with utilities specific for Win32 platform

Raises:
    ImportError: import error if implementation is not available for platform
"""


# ruff and mypy per file settings
#
# empty lines
# ruff: noqa: E302, E303
# naming conventions
# ruff: noqa: N801, N802, N803, N806, N812, N813, N815, N816, N818, N999
#
# disable mypy errors
# mypy: disable-error-code = "assignment"

# fmt: off



# version determination - latest import requirement for hatch-vcs-footgun-example
from utils_mystuff_windows.version import __version__

import sys
import os


if os.name == "nt" or sys.platform == "win32":
    from .utils_win32 import *
else:
    raise ImportError(f"No implementation of window utilities available for your platform ('{os.name}').")
