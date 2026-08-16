"""Smoke tests for the basic cover generation pipeline."""

from PIL import Image

from autocover.core import CoverGenerator
from autocover.renderer import TextRenderer


def test_generate_solid_cover_with_text(tmp_path):
    """A solid background with a title should render and save without raising."""
    width, height = 800, 400
    generator = CoverGenerator(width=width, height=height)
    generator.create_base("#111111")

    renderer = TextRenderer(generator.draw, generator.width, generator.height, generator.image)
    renderer.draw_text(
        "Hello World",
        "north",
        color="#ff7f00",
        text_type="title",
    )

    output_path = tmp_path / "cover.png"
    generator.save(str(output_path))

    assert output_path.exists()

    with Image.open(output_path) as img:
        assert img.size == (width, height)
