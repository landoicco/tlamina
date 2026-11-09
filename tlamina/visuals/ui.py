from tlamina.resources import load_font


def draw_text(surface, text, size, color='white', **position):
    """Draw text placed by a rect keyword, for example center=(x, y) or topleft=(x, y)."""
    text_surface = load_font(size).render(text, True, color)
    surface.blit(text_surface, text_surface.get_rect(**position))
