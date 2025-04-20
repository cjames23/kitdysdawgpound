import pygame


def create_bin_texts(bin_texts, text_color, font_size, font_name="Gill Sans", bold=True):
    """Create text surfaces for bin labels.

    Args:
        bin_texts: List of strings to render
        text_color: RGB color tuple for text
        font_size: Font size in pixels
        font_name: Font name to use
        bold: Whether to use bold font

    Returns:
        List of rendered text surfaces
    """
    bin_text_surfaces = []
    font = pygame.font.SysFont(font_name, font_size, bold)

    for text in bin_texts:
        rendered_text = font.render(text, True, text_color)
        bin_text_surfaces.append(rendered_text)

    return bin_text_surfaces
