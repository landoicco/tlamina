import json
import tomllib
from pathlib import Path

import pygame
import pytest

import resources
from enemy import Alien, Ufo
from game import Game
from laser import Laser
from settings import UFO_SPRITES

ROOT = Path(__file__).resolve().parent.parent


def manifest_names():
    with open(ROOT / 'tools' / 'atlas.toml', 'rb') as file:
        groups = tomllib.load(file)['sprites']
    return {name for group in groups.values() for name in group}


def test_atlas_matches_the_manifest():
    # Fails if tools/atlas.toml was edited without rebuilding the atlas
    index = json.loads((ROOT / 'assets' / 'atlas.json').read_text())['sprites']
    assert set(index) == manifest_names()


def test_atlas_rects_fit_inside_the_image():
    width, height = pygame.image.load(ROOT / 'assets' / 'atlas.png').get_size()
    for name, (x, y, w, h) in resources.load_atlas_index().items():
        assert x >= 0 and y >= 0 and x + w <= width and y + h <= height, name


def test_every_sprite_the_game_uses_is_in_the_atlas(monkeypatch, keys):
    requested = set()
    load_sprite = resources.load_sprite

    def recording_load_sprite(name, *args):
        requested.add(name)
        return load_sprite(name, *args)

    # Patch the name each sprite module imported, then create every kind of sprite
    for module in ('enemy', 'game', 'laser', 'obstacle', 'player'):
        monkeypatch.setattr(f'{module}.load_sprite', recording_load_sprite)
    Game()
    for color in UFO_SPRITES:
        Ufo(color, 0, 0)
    Alien('left')
    Laser((0, 0), 1)

    assert requested
    assert requested <= manifest_names()


def test_missing_sprite_names_the_fix():
    with pytest.raises(KeyError, match='tools/atlas.toml'):
        resources.load_sprite('notASprite')


@pytest.mark.parametrize('scale', [0.5, 0.6])
def test_sprite_scale(scale):
    original = resources.load_sprite('ufoRed', 1)
    scaled = resources.load_sprite('ufoRed', scale)

    # pygame truncates the scaled size
    assert scaled.get_width() == int(original.get_width() * scale)
    assert scaled.get_height() == int(original.get_height() * scale)
