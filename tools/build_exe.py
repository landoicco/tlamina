"""Build a Tlamina executable for the current platform with PyInstaller.

Usage: python tools/build_exe.py

Produces dist/tlamina-<platform>/ with the executable (Tlamina.app on macOS)
and the files that must ship with it (README, credits, licenses).
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

MACOS = platform.system() == 'Darwin'


def package_name():
    return 'tlamina-macos' if MACOS else f'tlamina-{platform.system().lower()}'


def build_executable():
    PyInstaller.__main__.run([
        str(ROOT / 'tlamina' / '__main__.py'),
        '--name', 'Tlamina',
        # A macOS app is a folder, and PyInstaller no longer supports single-file ones
        '--onedir' if MACOS else '--onefile',
        # No console window on Windows; on macOS, build Tlamina.app
        '--windowed',
        # The app's icon in Windows Explorer, the taskbar, and the macOS Finder and Dock;
        # Linux executables don't have one
        '--icon', str(ROOT / 'assets' / ('icon.icns' if MACOS else 'icon.ico')),
        '--osx-bundle-identifier', 'dev.licaza.tlamina',
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
    if MACOS:
        return BUILD / 'dist' / 'Tlamina.app'
    executable = 'Tlamina.exe' if platform.system() == 'Windows' else 'Tlamina'
    return BUILD / 'dist' / executable


def package(executable):
    target = DIST / package_name()
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True)
    if executable.is_dir():
        # Keep the app's internal symlinks, or its code signature breaks
        shutil.copytree(executable, target / executable.name, symlinks=True)
    else:
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
        relative = path.relative_to(target)
        # List the app bundle as one entry instead of its hundreds of files
        if relative.suffix == '.app':
            print(f'  {relative}/')
        elif path.is_file() and relative.parts[0] != 'Tlamina.app':
            print(f'  {relative}')


if __name__ == '__main__':
    main()
