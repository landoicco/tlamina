"""Pack the sprites listed in atlas.toml into assets/atlas.png and assets/atlas.json.

Usage: python tools/build_atlas.py --pack path/to/SpaceShooterRedux

The pack is read from a local folder; see tools/README.md for where to get it.
"""

import argparse
import json
import os
import sys
import tomllib
from pathlib import Path

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

import pygame

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'tools' / 'atlas.toml'
ATLAS_IMAGE = ROOT / 'assets' / 'atlas.png'
ATLAS_INDEX = ROOT / 'assets' / 'atlas.json'

ATLAS_WIDTH = 512
# Empty pixels between sprites, so scaling one sprite never samples its neighbors
PADDING = 2


def read_manifest():
    with open(MANIFEST, 'rb') as file:
        groups = tomllib.load(file)['sprites']
    names = [name for group in groups.values() for name in group]
    duplicates = {name for name in names if names.count(name) > 1}
    if duplicates:
        sys.exit(f'Duplicate sprites in {MANIFEST.name}: {", ".join(sorted(duplicates))}')
    return names


def find_sources(pack, names):
    files = {path.stem: path for path in (pack / 'PNG').rglob('*.png')}
    missing = [name for name in names if name not in files]
    if missing:
        sys.exit(f'Not found in {pack / "PNG"}: {", ".join(missing)}')
    return {name: files[name] for name in names}


def shelf_pack(sizes):
    """Place rectangles left to right in rows ("shelves"), tallest first."""
    positions = {}
    x = y = shelf_height = 0
    for name, (width, height) in sorted(sizes.items(), key=lambda item: (-item[1][1], item[0])):
        if width + PADDING > ATLAS_WIDTH:
            sys.exit(f'{name} is wider than the atlas ({width} px)')
        if x + width + PADDING > ATLAS_WIDTH:
            x, y, shelf_height = 0, y + shelf_height, 0
        positions[name] = (x + PADDING, y + PADDING)
        x += width + PADDING
        shelf_height = max(shelf_height, height + PADDING)
    return positions, y + shelf_height + PADDING


def build(pack):
    names = read_manifest()
    images = {name: pygame.image.load(path) for name, path in find_sources(pack, names).items()}
    positions, height = shelf_pack({name: image.get_size() for name, image in images.items()})

    atlas = pygame.Surface((ATLAS_WIDTH, height), pygame.SRCALPHA)
    rects = {}
    for name in names:
        image, (x, y) = images[name], positions[name]
        # Adding onto transparent pixels copies the source exactly; a normal
        # alpha blit would darken semi-transparent edges.
        atlas.blit(image, (x, y), special_flags=pygame.BLEND_RGBA_ADD)
        rects[name] = [x, y, *image.get_size()]

    pygame.image.save(atlas, ATLAS_IMAGE)
    write_index(rects)
    verify(images, rects)
    print(f'Packed {len(rects)} sprites into {ATLAS_IMAGE.relative_to(ROOT)} ({ATLAS_WIDTH}x{height})')


def write_index(rects):
    # One sprite per line keeps the file readable and its diffs small
    lines = [f'    {json.dumps(name)}: {json.dumps(rect)}' for name, rect in rects.items()]
    ATLAS_INDEX.write_text(
        '{\n'
        '  "source": "Space Shooter Redux by Kenney (www.kenney.nl), CC0. See assets/kenney/license.txt",\n'
        '  "sprites": {\n' + ',\n'.join(lines) + '\n  }\n}\n'
    )


def verify(images, rects):
    """Reload the saved atlas and check every sprite matches its source pixel for pixel."""
    saved = pygame.image.load(ATLAS_IMAGE)
    for name, rect in rects.items():
        packed = pygame.image.tobytes(saved.subsurface(rect), 'RGBA')
        if packed != pygame.image.tobytes(images[name], 'RGBA'):
            sys.exit(f'{name} does not match its source after packing')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--pack', type=Path, required=True, help="folder of the unzipped Space Shooter Redux pack")
    args = parser.parse_args()
    if not (args.pack / 'PNG').is_dir():
        sys.exit(f'{args.pack} does not look like the Space Shooter Redux pack (no PNG folder)')
    build(args.pack)


if __name__ == '__main__':
    main()
