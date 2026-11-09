import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_game_runs_headless(tmp_path):
    env = {
        **os.environ,
        'SDL_VIDEODRIVER': 'dummy',
        'SDL_AUDIODRIVER': 'dummy',
        'TLAMINA_MAX_FRAMES': '120',
        'TLAMINA_DATA_DIR': str(tmp_path / 'data'),
        # Only the package is found this way; the working directory stays unrelated
        'PYTHONPATH': str(ROOT),
    }
    # Run from an unrelated directory to make sure asset paths don't depend on it
    result = subprocess.run(
        [sys.executable, '-m', 'tlamina'],
        check=False,
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
