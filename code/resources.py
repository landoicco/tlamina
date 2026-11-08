import json
import sys
from functools import cache
from pathlib import Path

import pygame

from settings import SPRITE_SCALE

# PyInstaller unpacks bundled files into sys._MEIPASS; otherwise use the repo root.
ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))


def asset_path(relative_path):
    return str(ROOT / relative_path)


# Cached surfaces are shared between sprites, so don't draw on them directly
@cache
def load_image(relative_path):
    return pygame.image.load(asset_path(relative_path)).convert_alpha()


@cache
def load_atlas_index():
    with open(asset_path('assets/atlas.json')) as file:
        return json.load(file)['sprites']


@cache
def load_sprite(name, scale=SPRITE_SCALE):
    """Cut a sprite out of the atlas by its name in tools/atlas.toml."""
    index = load_atlas_index()
    if name not in index:
        raise KeyError(f"Sprite '{name}' is not in the atlas; add it to tools/atlas.toml and rebuild")
    sprite = load_image('assets/atlas.png').subsurface(index[name])
    if scale != 1:
        return pygame.transform.smoothscale_by(sprite, scale)
    # A copy, so the sprite doesn't keep the whole atlas locked or referenced
    return sprite.copy()


@cache
def load_sound(relative_path, volume):
    sound = pygame.mixer.Sound(asset_path(relative_path))
    sound.set_volume(volume)
    return sound
