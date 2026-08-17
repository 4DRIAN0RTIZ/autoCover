"""Command-line interface for autoCover."""

import argparse
import os
import sys

from .core import CoverGenerator
from .renderer import TextRenderer


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate blog cover images (OG images)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --title "My Title" --subtitle "Subtitle" --output cover.png
  %(prog)s --title "Title" --gradient "#111111,#ff7f00" --output cover.png
  %(prog)s --title "Title" --background bg.png --overlay 0.6 --output cover.png
        """
    )

    parser.add_argument("--title", type=str, help="Main title text")
    parser.add_argument("--subtitle", type=str, help="Subtitle text (center)")
    parser.add_argument("--footer", type=str, help="Footer text (bottom)")

    parser.add_argument("--output", "-o", type=str, default="cover.png",
                       help="Output file path (default: cover.png)")
    parser.add_argument("--width", type=int, default=1280,
                       help="Image width (default: 1280)")
    parser.add_argument("--height", type=int, default=720,
                       help="Image height (default: 720)")

    parser.add_argument("--bg-color", type=str, default="#111111",
                       help="Background color in hex (default: #111111)")
    parser.add_argument("--gradient", type=str,
                       help="Gradient colors: start,end (e.g., '#111111,#ff7f00')")
    parser.add_argument("--gradient-direction", type=str,
                       choices=["vertical", "horizontal"], default="vertical",
                       help="Gradient direction (default: vertical)")
    parser.add_argument("--background", type=str,
                       help="Path to background image")
    parser.add_argument("--overlay", type=float,
                       help="Overlay opacity 0-1 (for background images)")
    parser.add_argument("--overlay-color", type=str, default="#000000",
                       help="Overlay color in hex (default: #000000)")

    parser.add_argument("--text-color", type=str, default="#ff7f00",
                       help="Text color in hex (default: #ff7f00)")
    parser.add_argument("--font", type=str,
                       help="Path to custom font file (TTF/OTF)")
    parser.add_argument("--font-size-title", type=int,
                       help="Title font size (default: auto)")
    parser.add_argument("--font-size-subtitle", type=int,
                       help="Subtitle font size (default: auto)")
    parser.add_argument("--font-size-footer", type=int,
                       help="Footer font size (default: auto)")
    parser.add_argument("--title-max-lines", type=int, default=1,
                       help="Max lines for title before wrapping (default: 1)")
    parser.add_argument("--subtitle-max-lines", type=int, default=3,
                       help="Max lines for subtitle before wrapping (default: 3)")
    parser.add_argument("--no-shadow", action="store_true",
                       help="Disable text shadow")
    parser.add_argument("--max-width-ratio", type=float, default=0.9,
                       help="Max text area width as ratio of image width (default: 0.9)")
    parser.add_argument("--logo-gap", type=int, default=30,
                       help="Gap in pixels between logo and text area when avoiding "
                            "overlap (default: 30)")
    parser.add_argument("--logo-avoid-min-ratio", type=float, default=0.4,
                       help="Minimum allowed text area width (as ratio of image width) "
                            "when dodging the logo, below which avoidance is skipped "
                            "(default: 0.4)")

    parser.add_argument("--box", action="store_true",
                       help="Enable text boxes with rounded borders")
    parser.add_argument("--box-fill", type=str,
                       help="Box background color (hex, with alpha: #RRGGBBAA)")
    parser.add_argument("--box-border", type=str, default="#ff7f00",
                       help="Box border color (default: #ff7f00)")
    parser.add_argument("--box-border-width", type=int, default=3,
                       help="Box border width (default: 3)")
    parser.add_argument("--box-padding", type=int, default=30,
                       help="Box padding (default: 30)")
    parser.add_argument("--box-radius", type=int, default=20,
                       help="Box corner radius (default: 20)")

    parser.add_argument("--logo", type=str,
                       help="Path to logo image")
    parser.add_argument("--logo-size", type=int, default=100,
                       help="Logo size in pixels (default: 100)")
    parser.add_argument("--logo-position", type=str,
                       choices=["top-right", "top-left", "bottom-right", "bottom-left"],
                       default="top-right",
                       help="Logo position (default: top-right)")

    return parser.parse_args()


def generate_cover(*, title=None, subtitle=None, footer=None, output="cover.png",
                    width=1280, height=720, bg_color="#111111", gradient=None,
                    gradient_direction="vertical", background=None, overlay=None,
                    overlay_color="#000000", text_color="#ff7f00", font=None,
                    font_size_title=None, font_size_subtitle=None, font_size_footer=None,
                    title_max_lines=1, subtitle_max_lines=3, no_shadow=False,
                    max_width_ratio=0.9, logo_gap=30, logo_avoid_min_ratio=0.4,
                    box=False, box_fill=None, box_border="#ff7f00", box_border_width=3,
                    box_padding=30, box_radius=20, logo=None, logo_size=100,
                    logo_position="top-right"):
    """Generate a cover image and return the output path.

    Same parameters as the CLI flags. Raises ValueError on bad input.
    """
    if not any([title, subtitle, footer]):
        raise ValueError("At least one of title, subtitle, or footer is required")

    generator = CoverGenerator(width=width, height=height)

    if background:
        if not os.path.exists(background):
            raise ValueError(f"Background image not found: {background}")
        generator.load_background(background)
        if overlay is not None:
            generator.add_overlay(overlay_color, overlay)
    elif gradient:
        colors = gradient.split(",")
        if len(colors) != 2:
            raise ValueError("Gradient requires exactly 2 colors separated by comma")
        generator.create_gradient(colors[0].strip(), colors[1].strip(), gradient_direction)
    else:
        generator.create_base(bg_color)

    logo_rect = None
    if logo:
        if not os.path.exists(logo):
            print(f"Warning: Logo file not found: {logo}")
        else:
            logo_rect = generator.add_logo(logo, logo_size, logo_position)

    renderer = TextRenderer(generator.draw, generator.width, generator.height, generator.image)

    shadow_enabled = not no_shadow

    title_bottom = None
    if title:
        title_bottom = renderer.draw_text(title, "north",
                         font_path=font,
                         font_size=font_size_title,
                         color=text_color,
                         text_type="title",
                         shadow=shadow_enabled,
                         max_lines=title_max_lines,
                         box=box,
                         box_fill=box_fill,
                         box_border=box_border if box else None,
                         box_border_width=box_border_width,
                         box_padding=box_padding,
                         box_radius=box_radius,
                         avoid_rect=logo_rect,
                         max_width_ratio=max_width_ratio,
                         logo_gap=logo_gap,
                         logo_avoid_min_ratio=logo_avoid_min_ratio)

    if subtitle:
        renderer.draw_text(subtitle, "center",
                         font_path=font,
                         font_size=font_size_subtitle,
                         color=text_color,
                         text_type="subtitle",
                         shadow=shadow_enabled,
                         max_lines=subtitle_max_lines,
                         y_start=title_bottom,
                         box=box,
                         box_fill=box_fill,
                         box_border=box_border if box else None,
                         box_border_width=box_border_width,
                         box_padding=box_padding,
                         box_radius=box_radius,
                         avoid_rect=logo_rect,
                         max_width_ratio=max_width_ratio,
                         logo_gap=logo_gap,
                         logo_avoid_min_ratio=logo_avoid_min_ratio)

    if footer:
        renderer.draw_text(footer, "south",
                         font_path=font,
                         font_size=font_size_footer,
                         color=text_color,
                         text_type="footer",
                         shadow=shadow_enabled,
                         box=box,
                         box_fill=box_fill,
                         box_border=box_border if box else None,
                         box_border_width=box_border_width,
                         box_padding=box_padding,
                         box_radius=box_radius,
                         avoid_rect=logo_rect,
                         max_width_ratio=max_width_ratio,
                         logo_gap=logo_gap,
                         logo_avoid_min_ratio=logo_avoid_min_ratio)

    generator.save(output)
    return output


def main():
    """Main execution function"""
    args = parse_arguments()

    try:
        output = generate_cover(**vars(args))
        print(f"Cover image generated: {output}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error generating image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
