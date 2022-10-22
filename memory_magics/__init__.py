__submodules__ = [
    "memory_magics",
    "utils",
]

from ._version import __version__
from .memory_magics import load_ipython_extension

__all__ = ["load_ipython_extension", "__version__"]
