import os
from typing import Optional, Tuple

from PIL import Image, ImageDraw


class CoverGenerator:
    """Core image generation class for blog covers"""

    def __init__(self, width: int = 1280, height: int = 720):
        self.width = width
        self.height = height
        self.image = None
        self.draw = None

    def create_base(self, bg_color: str = "#111111") -> None:
        """Create base image with solid color"""
        self.image = Image.new("RGB", (self.width, self.height), bg_color)
        self.draw = ImageDraw.Draw(self.image)

    def create_gradient(self, color_start: str, color_end: str,
                       direction: str = "vertical") -> None:
        """Create gradient background"""
        self.image = Image.new("RGB", (self.width, self.height))

        start_rgb = self._hex_to_rgb(color_start)
        end_rgb = self._hex_to_rgb(color_end)

        if direction == "vertical":
            for y in range(self.height):
                ratio = y / self.height
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

                for x in range(self.width):
                    self.image.putpixel((x, y), (r, g, b))
        else:
            for x in range(self.width):
                ratio = x / self.width
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

                for y in range(self.height):
                    self.image.putpixel((x, y), (r, g, b))

        self.draw = ImageDraw.Draw(self.image)

    def load_background(self, image_path: str) -> None:
        """Load custom background image"""
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        self.image = bg_image.convert("RGB")
        self.draw = ImageDraw.Draw(self.image)

    def add_overlay(self, color: str = "#000000", opacity: float = 0.5) -> None:
        """Add semi-transparent overlay"""
        overlay = Image.new("RGBA", (self.width, self.height), color)
        overlay.putalpha(int(255 * opacity))

        base = self.image.convert("RGBA")
        base = Image.alpha_composite(base, overlay)
        self.image = base.convert("RGB")
        self.draw = ImageDraw.Draw(self.image)

    def add_logo(self, logo_path: str, size: int = 100,
                position: str = "top-right") -> Optional[Tuple[int, int, int, int]]:
        """Add logo to the image. Returns (x1, y1, x2, y2) bounding box or None."""
        if not os.path.exists(logo_path):
            return None

        logo = Image.open(logo_path)
        logo.thumbnail((size, size), Image.Resampling.LANCZOS)

        if logo.mode != "RGBA":
            logo = logo.convert("RGBA")

        margin = 40
        if position == "top-right":
            pos = (self.width - logo.width - margin, margin)
        elif position == "top-left":
            pos = (margin, margin)
        elif position == "bottom-right":
            pos = (self.width - logo.width - margin,
                  self.height - logo.height - margin)
        elif position == "bottom-left":
            pos = (margin, self.height - logo.height - margin)
        else:
            pos = (self.width - logo.width - margin, margin)

        self.image.paste(logo, pos, logo)
        self.draw = ImageDraw.Draw(self.image)

        return (pos[0], pos[1], pos[0] + logo.width, pos[1] + logo.height)

    def save(self, output_path: str) -> None:
        """Save the generated image"""
        ext = output_path.lower().split('.')[-1]

        if ext == 'webp':
            self.image.save(output_path, format='WEBP', quality=90, method=6)
        elif ext in ['jpg', 'jpeg']:
            self.image.save(output_path, format='JPEG', quality=95, optimize=True)
        else:
            self.image.save(output_path, quality=95, optimize=True)

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
