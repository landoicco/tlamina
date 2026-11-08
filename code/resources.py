import sys
from functools import cache
from pathlib import Path

import pygame

# PyInstaller unpacks bundled files into sys._MEIPASS; otherwise use the repo root.
ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))


def asset_path(relative_path):
    return str(ROOT / relative_path)


# Cached surfaces are shared between sprites, so don't draw on them directly
@cache
def load_image(relative_path):
    return pygame.image.load(asset_path(relative_path)).convert_alpha()


@cache
def load_sound(relative_path, volume):
    sound = pygame.mixer.Sound(asset_path(relative_path))
    sound.set_volume(volume)
    return sound
