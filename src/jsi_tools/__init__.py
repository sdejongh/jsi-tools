"""jsi_tools — Personal Python utility library."""

from __future__ import annotations

__version__ = "0.2.0"

from jsi_tools.decorators import log_return
from jsi_tools.helpers import DictDiff, ListDiff, SetDiff, diff

__all__ = ["DictDiff", "ListDiff", "SetDiff", "diff", "log_return"]
