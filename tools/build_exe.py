"""Build a single-file Tlamina executable for the current platform with PyInstaller.

Usage: python tools/build_exe.py

Produces dist/tlamina-<platform>/ with the executable and the files that must
ship with it (README, credits, licenses).
"""

import os
import platform
import shutil
from pathlib import Path

import PyInstaller.__main__

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / 'build' / 'pyinstaller'
DIST = ROOT / 'dist'

# Shipped next to the executable in every package
PACKAGE_FILES = ['README.md', 'CREDITS.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'licenses']


def package_name():
    return f'tlamina-{platform.system().lower()}'


def build_executable():
    PyInstaller.__main__.run([
        str(ROOT / 'tlamina' / '__main__.py'),
        '--name', 'Tlamina',
        '--onefile',
        # No console window on Windows
        '--windowed',
        # __main__.py imports the rest of the tlamina package, found from the repo root
        '--paths', str(ROOT),
        # Bundled under sys._MEIPASS/assets, where resources.py looks for them
        '--add-data', f'{ROOT / "assets"}{os.pathsep}assets',
        '--distpath', str(BUILD / 'dist'),
        '--workpath', str(BUILD / 'work'),
        '--specpath', str(BUILD),
        '--noconfirm',
        '--clean',
    ])
    executable = 'Tlamina.exe' if platform.system() == 'Windows' else 'Tlamina'
    return BUILD / 'dist' / executable


def package(executable):
    target = DIST / package_name()
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True)
    shutil.copy2(executable, target)
    for name in PACKAGE_FILES:
        source = ROOT / name
        if source.is_dir():
            shutil.copytree(source, target / name)
        else:
            shutil.copy2(source, target)
    return target


def main():
    target = package(build_executable())
    print(f'Packaged {target.relative_to(ROOT)}:')
    for path in sorted(target.rglob('*')):
        if path.is_file():
            print(f'  {path.relative_to(target)}')


if __name__ == '__main__':
    main()
