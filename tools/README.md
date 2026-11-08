# 🛠️ Tools

## 🗺️ Sprite atlas

All sprites in the game come from one image, `assets/atlas.png`, with their positions listed in `assets/atlas.json`. Only the sprites listed in [`atlas.toml`](atlas.toml) are packed, at their original size and quality.

Both generated files are committed, so the game never needs the source pack. You only need it to add or change sprites.

### Get the source pack

The sprites come from **Space Shooter Redux** by Kenney, released under CC0 (see [`assets/kenney/space-shooter-redux/license.txt`](../assets/kenney/space-shooter-redux/license.txt)):

- Original: [kenney.nl/assets/space-shooter-redux](https://kenney.nl/assets/space-shooter-redux)
- Mirror: [opengameart.org/content/space-shooter-redux](https://opengameart.org/content/space-shooter-redux)

The atlas was built from the OpenGameArt `SpaceShooterRedux.zip`, with this SHA-256:

```
d44a371a8fa1eb5d61a4fed3677954590aa015a78d2afb5f97924cfe02e3f700
```

Check a download with `sha256sum SpaceShooterRedux.zip`. A different hash doesn't necessarily mean the sprites changed, but the script's output may then differ from the committed atlas.

### Add a sprite

1. Find the sprite's file name in the pack's `PNG/` folder, for example `PNG/Meteors/meteorBrown_med1.png`.
2. Add its name without the extension to `atlas.toml`: `'meteorBrown_med1'`.
3. Rebuild the atlas (requires Python 3.11+ and pygame-ce, both in `nix develop`):

   ```sh
   python tools/build_atlas.py --pack path/to/unzipped/SpaceShooterRedux
   ```

4. Commit `atlas.toml`, `assets/atlas.png`, and `assets/atlas.json` together.

The script checks that every packed sprite matches its source pixel for pixel, and fails if a name is missing or duplicated.
