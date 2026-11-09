import os
import sys
from collections import defaultdict
from pathlib import Path

import pytest

# Must be set before pygame creates a window or opens an audio device
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'code'))

import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


@pytest.fixture(scope='session', autouse=True)
def pygame_display():
    pygame.init()
    # Images can only be converted once a display mode is set
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    yield
    pygame.quit()


@pytest.fixture(autouse=True)
def data_dir(monkeypatch, tmp_path):
    """Keep saved data, like the high score, out of the real user folder."""
    path = tmp_path / 'data'
    monkeypatch.setenv('TLAMINA_DATA_DIR', str(path))
    return path


@pytest.fixture
def keys(monkeypatch):
    """Keys held down during the test; add pygame key constants to press them."""
    pressed = set()
    monkeypatch.setattr(pygame.key, 'get_pressed', lambda: defaultdict(bool, dict.fromkeys(pressed, True)))
    return pressed


@pytest.fixture
def game(keys):
    from game import Game

    return Game()
