# 🧑‍💻 Development

How to run Tlamina from source, test it, and build and release the executables. How the code is organized is in the [architecture](architecture.md) page.

## 🚀 Running from source

Requires Python 3.11 or newer. With [uv](https://docs.astral.sh/uv/):

```sh
uv run python -m tlamina
```

Or with Nix: `nix develop`, then `python -m tlamina`.

## 🧪 Lint and tests

Inside `nix develop`, or prefixed with `uv run`:

```sh
ruff check .
pytest
```

## 📦 Executables

To build an executable for your platform:

```sh
uv run --group build python tools/build_exe.py
```

The result goes to `dist/tlamina-<platform>/`, with the README, credits, and licenses next to it. On macOS it's `Tlamina.app`; on Linux and Windows, a single file.

The sprite atlas has its own script, described in [`tools/README.md`](../tools/README.md).

## ⚙️ CI and releases

On every pull request and push to `master`, [`ci.yml`](../.github/workflows/ci.yml) runs the lint and tests, then builds the executables for Linux, Windows, and macOS and smoke-tests each one by running it headless for 120 frames. The builds are kept as workflow artifacts for 14 days.

To release a new version:

1. Bump `version` in `pyproject.toml` on the branch. It's the only place the version lives: the splash screen reads it from there.
2. Merge the pull request.
3. Tag the merge commit on `master` as `vX.Y.Z` and push the tag.

[`release.yml`](../.github/workflows/release.yml) then checks that the tag matches `pyproject.toml`, builds the three executables, and publishes them as a GitHub release.
