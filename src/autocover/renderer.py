import os
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont


class TextRenderer:
    """Handle text rendering with adaptive sizing and effects"""

    DEFAULT_FONT_SIZES = {
        "title": 100,
        "subtitle": 60,
        "footer": 48
    }

    def __init__(self, draw: ImageDraw.Draw, image_width: int, image_height: int,
                 image: Optional[Image.Image] = None):
        self.draw = draw
        self.image_width = image_width
        self.image_height = image_height
        self.image = image

    def draw_text(self, text: str, position: str,
                 font_path: Optional[str] = None,
                 font_size: Optional[int] = None,
                 color: str = "#ff7f00",
                 text_type: str = "title",
                 shadow: bool = True,
                 max_width_ratio: float = 0.9,
                 max_lines: int = 1,
                 y_start: Optional[int] = None,
                 box: bool = False,
                 box_fill: Optional[str] = None,
                 box_border: Optional[str] = None,
                 box_border_width: int = 3,
                 box_padding: int = 30,
                 box_radius: int = 20,
                 avoid_rect: Optional[Tuple[int, int, int, int]] = None,
                 logo_gap: int = 30,
                 logo_avoid_min_ratio: float = 0.4) -> Optional[int]:
        """Draw text with automatic sizing, wrapping, and optional shadow and box.
        avoid_rect: (x1, y1, x2, y2) zone (e.g. logo bbox) the text area must not overlap.
        logo_gap: pixels of breathing room kept between avoid_rect and the text area.
        logo_avoid_min_ratio: minimum text-area width (as a ratio of image width) allowed
        when dodging avoid_rect; below this, avoidance is skipped and full width is used.
        Returns the bottom y coordinate of the drawn element."""

        if not text:
            return None

        if font_size is None:
            font_size = self.DEFAULT_FONT_SIZES.get(text_type, 60)

        font = self._load_font(font_path, font_size, text_type)

        avail_x1, avail_x2 = self._get_available_x_range(
            text_type, position, y_start, avoid_rect, logo_gap, logo_avoid_min_ratio
        )
        avail_width = avail_x2 - avail_x1

        max_width = min(int(self.image_width * max_width_ratio), avail_width)

        if box:
            max_width = (min(int(self.image_width * max_width_ratio), avail_width)
                         - (box_padding * 2))

        # Intelligent sizing: try single line first, wrap only if font would shrink too much
        if text_type != "footer":
            single_font, single_size = self._fit_text_to_width(
                text, font, font_path, font_size, max_width, text_type
            )
            # Wrap if single-line requires more than 25% font reduction and wrapping is allowed
            if single_size < font_size * 0.75 and max_lines > 1:
                zone_height = self._get_zone_height(position, y_start)
                # Allow subtitle to scale up to 80% of title size at most
                title_size = self.DEFAULT_FONT_SIZES.get("title", 100)
                zone_start = max(font_size, int(title_size * 0.80))
                font, font_size, lines = self._fit_to_zone(
                    text, font_path, zone_start, max_width, zone_height, max_lines, text_type
                )
            else:
                font = single_font
                font_size = single_size
                lines = [text]
        else:
            font, font_size = self._fit_text_to_width(
                text, font, font_path, font_size, max_width, text_type
            )
            lines = [text]

        line_bboxes = [self.draw.textbbox((0, 0), line, font=font) for line in lines]
        line_heights = [bb[3] - bb[1] for bb in line_bboxes]
        line_widths = [bb[2] - bb[0] for bb in line_bboxes]
        line_spacing = max(4, font_size // 10)
        total_height = sum(line_heights) + line_spacing * (len(lines) - 1)
        max_line_width = max(line_widths)

        if len(lines) == 1:
            x, y = self._calculate_position(position, line_widths[0], line_heights[0], text_type,
                                            y_start, avail_x1, avail_x2)
        else:
            x = avail_x1 + (avail_width - max_line_width) // 2
            _, y = self._calculate_position(position, max_line_width, total_height, text_type,
                                            y_start, avail_x1, avail_x2)

        # Ensure a visible gap between stacked elements when both have boxes
        if box and y_start is not None:
            y = max(y, y_start + box_padding + 12)

        if box:
            box_x1 = x - box_padding
            box_y1 = y - box_padding
            box_x2 = x + max_line_width + box_padding
            box_y2 = y + total_height + box_padding

            has_alpha = box_fill and len(box_fill.lstrip("#")) == 8

            if has_alpha and self.image:
                overlay = Image.new("RGBA", (self.image_width, self.image_height), (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)

                self._draw_rounded_rectangle_on_draw(
                    overlay_draw,
                    (box_x1, box_y1, box_x2, box_y2),
                    radius=box_radius,
                    fill=box_fill,
                    outline=box_border,
                    width=box_border_width
                )

                cur_y = y
                for i, line in enumerate(lines):
                    lx = avail_x1 + (avail_width - line_widths[i]) // 2 if len(lines) > 1 else x
                    overlay_draw.text((lx, cur_y), line, font=font, fill=color)
                    cur_y += line_heights[i] + line_spacing

                base = self.image.convert("RGBA")
                self.image.paste(Image.alpha_composite(base, overlay).convert("RGB"))
                self.draw = ImageDraw.Draw(self.image)
            else:
                self._draw_rounded_rectangle(
                    (box_x1, box_y1, box_x2, box_y2),
                    radius=box_radius,
                    fill=box_fill,
                    outline=box_border,
                    width=box_border_width
                )
                cur_y = y
                for i, line in enumerate(lines):
                    lx = avail_x1 + (avail_width - line_widths[i]) // 2 if len(lines) > 1 else x
                    self.draw.text((lx, cur_y), line, font=font, fill=color)
                    cur_y += line_heights[i] + line_spacing
        else:
            shadow_offset = max(2, font_size // 40)
            cur_y = y
            for i, line in enumerate(lines):
                lx = avail_x1 + (avail_width - line_widths[i]) // 2 if len(lines) > 1 else x
                if shadow:
                    self.draw.text(
                        (lx + shadow_offset, cur_y + shadow_offset),
                        line, font=font, fill="#000000"
                    )
                self.draw.text((lx, cur_y), line, font=font, fill=color)
                cur_y += line_heights[i] + line_spacing

        # Return bottom y for layout chaining
        if box:
            return y + total_height + box_padding
        return y + total_height

    def _load_font(self, font_path: Optional[str], size: int,
                   text_type: str = "title") -> ImageFont.FreeTypeFont:
        """Load font or fallback to default"""
        if text_type == "footer":
            default_fonts = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
                "/System/Library/Fonts/Monaco.ttf",
                "C:\\Windows\\Fonts\\consola.ttf"
            ]
            try:
                for font in default_fonts:
                    if os.path.exists(font):
                        return ImageFont.truetype(font, size)
            except Exception:
                pass
            return ImageFont.load_default()

        if font_path and os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass

        try:
            default_fonts = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "C:\\Windows\\Fonts\\arial.ttf"
            ]
            for font in default_fonts:
                if os.path.exists(font):
                    return ImageFont.truetype(font, size)
        except Exception:
            pass

        return ImageFont.load_default()

    def _fit_text_to_width(self, text: str, font: ImageFont.FreeTypeFont,
                          font_path: Optional[str], font_size: int,
                          max_width: int,
                          text_type: str = "title") -> Tuple[ImageFont.FreeTypeFont, int]:
        """Adjust font size to fit text within max width"""

        bbox = self.draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]

        while text_width > max_width and font_size > 20:
            font_size -= 2
            font = self._load_font(font_path, font_size, text_type)
            bbox = self.draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]

        return font, font_size

    def _get_zone_height(self, position: str, y_start: Optional[int] = None) -> int:
        """Return the available vertical height for a given position"""
        if position in ("north", "top"):
            return int(self.image_height * 0.28)
        elif position in ("center", "middle"):
            # Available height between end of previous element and start of footer
            top = y_start + 20 if y_start is not None else int(self.image_height * 0.30)
            footer_top = int(self.image_height * 0.87)
            return max(int(self.image_height * 0.20), footer_top - top)
        elif position in ("south", "bottom"):
            return int(self.image_height * 0.20)
        return int(self.image_height * 0.40)

    def _fit_to_zone(self, text: str, font_path: Optional[str], font_size: int,
                     max_width: int, max_height: int, max_lines: int,
                     text_type: str) -> Tuple[ImageFont.FreeTypeFont, int, list]:
        """Find the largest font where wrapped text fits within max_width and max_height"""
        font = self._load_font(font_path, font_size, text_type)
        lines = self._wrap_text_to_lines(text, font, max_width)

        while font_size > 20:
            line_bboxes = [self.draw.textbbox((0, 0), ln, font=font) for ln in lines]
            line_heights = [bb[3] - bb[1] for bb in line_bboxes]
            line_widths = [bb[2] - bb[0] for bb in line_bboxes]
            line_spacing = max(4, font_size // 10)
            total_h = sum(line_heights) + line_spacing * (len(lines) - 1)
            max_lw = max(line_widths)

            if len(lines) <= max_lines and max_lw <= max_width and total_h <= max_height:
                return font, font_size, lines

            font_size -= 2
            font = self._load_font(font_path, font_size, text_type)
            lines = self._wrap_text_to_lines(text, font, max_width)

        return font, font_size, lines

    def _wrap_text_to_lines(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list:
        """Split text into lines that fit within max_width, breaking on word boundaries"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            bbox = self.draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)

        if current_line:
            lines.append(" ".join(current_line))

        return lines if lines else [text]

    def _get_available_x_range(self, text_type: str, position: str,
                              y_start: Optional[int] = None,
                              avoid_rect: Optional[Tuple[int, int, int, int]] = None,
                              gap: int = 30,
                              min_ratio: float = 0.4) -> Tuple[int, int]:
        """Return (x1, x2) horizontal range the text is allowed to occupy,
        narrowed to dodge avoid_rect (e.g. a logo) when their vertical zones overlap."""
        x1, x2 = 0, self.image_width

        if not avoid_rect:
            return x1, x2

        rect_x1, rect_y1, rect_x2, rect_y2 = avoid_rect

        zone_top, zone_bottom = self._get_zone_bounds(text_type, position, y_start)

        # Only reserve space if the text's vertical zone actually overlaps the logo's
        if zone_bottom < rect_y1 or zone_top > rect_y2:
            return x1, x2

        # Logo on the left half -> push text area right; on the right half -> push left
        if rect_x1 < self.image_width - rect_x2:
            x1 = rect_x2 + gap
        else:
            x2 = rect_x1 - gap

        if x2 - x1 < self.image_width * min_ratio:
            # Avoiding would leave too little room; fall back to full width
            return 0, self.image_width

        return x1, x2

    def _get_zone_bounds(self, text_type: str, position: str,
                         y_start: Optional[int] = None) -> Tuple[int, int]:
        """Approximate vertical (top, bottom) pixel bounds a text block will occupy."""
        if text_type == "footer":
            return int(self.image_height * 0.90), self.image_height

        if position in ("north", "top"):
            return 0, int(self.image_height * 0.35)
        elif position in ("center", "middle"):
            top = y_start if y_start is not None else int(self.image_height * 0.30)
            return top, int(self.image_height * 0.90)
        elif position in ("south", "bottom"):
            return int(self.image_height * 0.75), self.image_height

        return 0, self.image_height

    def _calculate_position(self, position: str,
                           text_width: int, text_height: int,
                           text_type: str = "title",
                           y_start: Optional[int] = None,
                           avail_x1: int = 0,
                           avail_x2: Optional[int] = None) -> Tuple[int, int]:
        """Calculate x, y coordinates based on position string"""

        if avail_x2 is None:
            avail_x2 = self.image_width

        if text_type == "footer":
            x = avail_x2 - text_width - 40
            x = max(x, avail_x1 + 10)
            y = self.image_height - text_height - 30
        else:
            x = avail_x1 + (avail_x2 - avail_x1 - text_width) // 2

            if position == "north" or position == "top":
                y = int(self.image_height * 0.08)
            elif position == "center" or position == "middle":
                if y_start is not None:
                    # Stack subtitle right after title with a gap
                    y = y_start + 30
                else:
                    # No title reference: center in the image
                    y = (self.image_height - text_height) // 2
            elif position == "south" or position == "bottom":
                y = self.image_height - text_height - 80
            else:
                y = (self.image_height - text_height) // 2

        return x, y

    def _draw_rounded_rectangle(self, coords: Tuple[int, int, int, int],
                               radius: int = 20,
                               fill: Optional[str] = None,
                               outline: Optional[str] = None,
                               width: int = 1) -> None:
        """Draw a rounded rectangle with support for RGBA colors"""
        self._draw_rounded_rectangle_on_draw(self.draw, coords, radius, fill, outline, width)

    @staticmethod
    def _draw_rounded_rectangle_on_draw(draw: ImageDraw.Draw,
                                       coords: Tuple[int, int, int, int],
                                       radius: int = 20,
                                       fill: Optional[str] = None,
                                       outline: Optional[str] = None,
                                       width: int = 1) -> None:
        """Draw a rounded rectangle on a specific draw object"""
        x1, y1, x2, y2 = coords

        if fill:
            fill_color = TextRenderer._parse_color(fill)
            draw.rounded_rectangle(
                [(x1, y1), (x2, y2)],
                radius=radius,
                fill=fill_color
            )

        if outline:
            outline_color = TextRenderer._parse_color(outline)
            draw.rounded_rectangle(
                [(x1, y1), (x2, y2)],
                radius=radius,
                outline=outline_color,
                width=width
            )

    @staticmethod
    def _parse_color(color: str):
        """Parse color string (hex RGB or RGBA) to tuple"""
        if not color:
            return None

        color = color.lstrip("#")

        if len(color) == 8:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            a = int(color[6:8], 16)
            return (r, g, b, a)
        elif len(color) == 6:
            return color if color.startswith("#") else f"#{color}"
        else:
            return color
