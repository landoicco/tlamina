import os
import subprocess
import sys
from pathlib import Path

MAIN = Path(__file__).resolve().parent.parent / 'code' / 'main.py'


def test_game_runs_headless(tmp_path):
    env = {
        **os.environ,
        'SDL_VIDEODRIVER': 'dummy',
        'SDL_AUDIODRIVER': 'dummy',
        'TLAMINA_MAX_FRAMES': '120',
        'TLAMINA_DATA_DIR': str(tmp_path / 'data'),
    }
    # Run from an unrelated directory to make sure asset paths don't depend on it
    result = subprocess.run(
        [sys.executable, str(MAIN)],
        check=False,
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
