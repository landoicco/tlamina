import json
import os
import sys
from pathlib import Path

FILE_NAME = 'highscore.json'


def data_dir():
    """Where the game keeps its saved data; TLAMINA_DATA_DIR overrides it, for tests."""
    if 'TLAMINA_DATA_DIR' in os.environ:
        return Path(os.environ['TLAMINA_DATA_DIR'])
    if sys.platform == 'win32':
        return Path(os.environ.get('APPDATA', Path.home())) / 'tlamina'
    if sys.platform == 'darwin':
        return Path.home() / 'Library' / 'Application Support' / 'tlamina'
    return Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share')) / 'tlamina'


def load_high_score():
    try:
        return int(json.loads((data_dir() / FILE_NAME).read_text())['high_score'])
    except (OSError, ValueError, KeyError, TypeError):
        # Missing or damaged file: start over rather than crash
        return 0


def save_high_score(score):
    try:
        data_dir().mkdir(parents=True, exist_ok=True)
        (data_dir() / FILE_NAME).write_text(json.dumps({'high_score': score}) + '\n')
    except OSError:
        # Losing the high score is better than crashing at the end of a run
        pass
