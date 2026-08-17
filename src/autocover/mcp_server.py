"""MCP server exposing autoCover as a tool for LLM clients."""

from typing import Optional

from mcp.server.fastmcp import FastMCP

from .cli import generate_cover

mcp = FastMCP("autocover")


@mcp.tool()
def generate_cover_image(
    output: str,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    footer: Optional[str] = None,
    width: int = 1280,
    height: int = 720,
    bg_color: str = "#111111",
    gradient: Optional[str] = None,
    gradient_direction: str = "vertical",
    background: Optional[str] = None,
    overlay: Optional[float] = None,
    overlay_color: str = "#000000",
    text_color: str = "#ff7f00",
    font: Optional[str] = None,
    font_size_title: Optional[int] = None,
    font_size_subtitle: Optional[int] = None,
    font_size_footer: Optional[int] = None,
    title_max_lines: int = 1,
    subtitle_max_lines: int = 3,
    no_shadow: bool = False,
    max_width_ratio: float = 0.9,
    logo_gap: int = 30,
    logo_avoid_min_ratio: float = 0.4,
    box: bool = False,
    box_fill: Optional[str] = None,
    box_border: str = "#ff7f00",
    box_border_width: int = 3,
    box_padding: int = 30,
    box_radius: int = 20,
    logo: Optional[str] = None,
    logo_size: int = 100,
    logo_position: str = "top-right",
) -> str:
    """Generate a blog cover (OG) image and save it to `output`.

    At least one of title, subtitle, or footer is required. Returns the
    absolute path of the generated file on success.
    """
    path = generate_cover(
        title=title,
        subtitle=subtitle,
        footer=footer,
        output=output,
        width=width,
        height=height,
        bg_color=bg_color,
        gradient=gradient,
        gradient_direction=gradient_direction,
        background=background,
        overlay=overlay,
        overlay_color=overlay_color,
        text_color=text_color,
        font=font,
        font_size_title=font_size_title,
        font_size_subtitle=font_size_subtitle,
        font_size_footer=font_size_footer,
        title_max_lines=title_max_lines,
        subtitle_max_lines=subtitle_max_lines,
        no_shadow=no_shadow,
        max_width_ratio=max_width_ratio,
        logo_gap=logo_gap,
        logo_avoid_min_ratio=logo_avoid_min_ratio,
        box=box,
        box_fill=box_fill,
        box_border=box_border,
        box_border_width=box_border_width,
        box_padding=box_padding,
        box_radius=box_radius,
        logo=logo,
        logo_size=logo_size,
        logo_position=logo_position,
    )
    return path


def main():
    mcp.run()


if __name__ == "__main__":
    main()
