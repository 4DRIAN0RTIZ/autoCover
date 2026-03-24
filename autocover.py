#!/usr/bin/env python3
"""
autoCover - Generate beautiful blog cover images from the command line
"""

import argparse
import sys
import os
from image_generator import CoverGenerator
from text_renderer import TextRenderer


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


def main():
    """Main execution function"""
    args = parse_arguments()

    if not any([args.title, args.subtitle, args.footer]):
        print("Error: At least one of --title, --subtitle, or --footer is required")
        sys.exit(1)

    try:
        generator = CoverGenerator(width=args.width, height=args.height)

        if args.background:
            if not os.path.exists(args.background):
                print(f"Error: Background image not found: {args.background}")
                sys.exit(1)
            generator.load_background(args.background)
            if args.overlay is not None:
                generator.add_overlay(args.overlay_color, args.overlay)
        elif args.gradient:
            try:
                colors = args.gradient.split(",")
                if len(colors) != 2:
                    print("Error: Gradient requires exactly 2 colors separated by comma")
                    sys.exit(1)
                generator.create_gradient(colors[0].strip(), colors[1].strip(),
                                        args.gradient_direction)
            except Exception as e:
                print(f"Error creating gradient: {e}")
                sys.exit(1)
        else:
            generator.create_base(args.bg_color)

        if args.logo:
            if not os.path.exists(args.logo):
                print(f"Warning: Logo file not found: {args.logo}")
            else:
                generator.add_logo(args.logo, args.logo_size, args.logo_position)

        renderer = TextRenderer(generator.draw, generator.width, generator.height, generator.image)

        shadow_enabled = not args.no_shadow

        title_bottom = None
        if args.title:
            title_bottom = renderer.draw_text(args.title, "north",
                             font_path=args.font,
                             font_size=args.font_size_title,
                             color=args.text_color,
                             text_type="title",
                             shadow=shadow_enabled,
                             max_lines=args.title_max_lines,
                             box=args.box,
                             box_fill=args.box_fill,
                             box_border=args.box_border if args.box else None,
                             box_border_width=args.box_border_width,
                             box_padding=args.box_padding,
                             box_radius=args.box_radius)

        if args.subtitle:
            renderer.draw_text(args.subtitle, "center",
                             font_path=args.font,
                             font_size=args.font_size_subtitle,
                             color=args.text_color,
                             text_type="subtitle",
                             shadow=shadow_enabled,
                             max_lines=args.subtitle_max_lines,
                             y_start=title_bottom,
                             box=args.box,
                             box_fill=args.box_fill,
                             box_border=args.box_border if args.box else None,
                             box_border_width=args.box_border_width,
                             box_padding=args.box_padding,
                             box_radius=args.box_radius)

        if args.footer:
            renderer.draw_text(args.footer, "south",
                             font_path=args.font,
                             font_size=args.font_size_footer,
                             color=args.text_color,
                             text_type="footer",
                             shadow=shadow_enabled,
                             box=args.box,
                             box_fill=args.box_fill,
                             box_border=args.box_border if args.box else None,
                             box_border_width=args.box_border_width,
                             box_padding=args.box_padding,
                             box_radius=args.box_radius)

        generator.save(args.output)
        print(f"Cover image generated: {args.output}")

    except Exception as e:
        print(f"Error generating image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
