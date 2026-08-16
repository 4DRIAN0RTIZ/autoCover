"""autoCover - Generate beautiful blog cover images from the command line."""

from .core import CoverGenerator
from .renderer import TextRenderer

__version__ = "0.1.0"

__all__ = ["CoverGenerator", "TextRenderer"]
