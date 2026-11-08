import sys
from pathlib import Path

# PyInstaller unpacks bundled files into sys._MEIPASS; otherwise use the repo root.
ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))


def asset_path(relative_path):
    return str(ROOT / relative_path)
