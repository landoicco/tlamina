# Third-party notices

The Tlamina executables are built with [PyInstaller](https://pyinstaller.org) and bundle the Python interpreter, [pygame-ce](https://pyga.me/), and the native libraries that pygame-ce ships with. They keep their own licenses, listed below. The source code of every component is available at the linked project pages.

This list was compiled from the pygame-ce 2.5.8 wheels for Windows, Linux, and macOS. Some libraries are only bundled on one platform.

For the game's art and audio, see [CREDITS.md](CREDITS.md).

## Runtime

| Component | License | Source |
|---|---|---|
| Python | [PSF License 2.0](https://docs.python.org/3/license.html) | [python.org](https://www.python.org) |
| PyInstaller bootloader | GPL-2.0 with an exception that allows distributing the built executable under any license | [pyinstaller.org](https://pyinstaller.org) |
| pygame-ce | LGPL-2.1 ([text](licenses/LGPL-2.1.txt)) | [github.com/pygame-community/pygame-ce](https://github.com/pygame-community/pygame-ce) |
| FreeSansBold font (bundled with pygame-ce, not used by the game) | GPL-3.0 with font exception ([text](licenses/GPL-3.0.txt)) | [GNU FreeFont](https://www.gnu.org/software/freefont/) |

## Native libraries

| Library | License | Platforms | Source |
|---|---|---|---|
| SDL2, SDL2_image, SDL2_mixer, SDL2_ttf | zlib | Windows, Linux, macOS | [libsdl.org](https://www.libsdl.org) |
| FreeType | FreeType License (FTL) | Windows, Linux, macOS | [freetype.org](https://freetype.org) |
| HarfBuzz | MIT | Linux, macOS | [harfbuzz.github.io](https://harfbuzz.github.io) |
| libpng | PNG Reference Library License v2 | Windows, Linux, macOS | [libpng.org](http://www.libpng.org/pub/png/libpng.html) |
| libjpeg-turbo | IJG, BSD-3-Clause, zlib | Windows, Linux, macOS | [libjpeg-turbo.org](https://libjpeg-turbo.org) |
| libtiff | libtiff license (BSD-style) | Windows, Linux, macOS | [libtiff.gitlab.io](https://libtiff.gitlab.io/libtiff/) |
| libwebp (incl. libsharpyuv, libwebpdemux) | BSD-3-Clause | Windows, Linux, macOS | [chromium.googlesource.com/webm/libwebp](https://chromium.googlesource.com/webm/libwebp) |
| libogg, libvorbis, libFLAC, libopus, libopusfile | BSD-3-Clause | Windows, Linux, macOS (libvorbis, libFLAC: not Windows) | [xiph.org](https://xiph.org) |
| WavPack | BSD-3-Clause | Windows, Linux, macOS | [wavpack.com](https://www.wavpack.com) |
| libxmp | MIT | Windows, Linux, macOS | [github.com/libxmp/libxmp](https://github.com/libxmp/libxmp) |
| PortMidi | MIT-style | Windows, Linux, macOS | [github.com/PortMidi/portmidi](https://github.com/PortMidi/portmidi) |
| mpg123 | LGPL-2.1 ([text](licenses/LGPL-2.1.txt)) | Linux, macOS | [mpg123.de](https://www.mpg123.de) |
| libsndfile | LGPL-2.1 ([text](licenses/LGPL-2.1.txt)) | Linux, macOS | [libsndfile.github.io](https://libsndfile.github.io/libsndfile/) |
| FluidSynth | LGPL-2.1 ([text](licenses/LGPL-2.1.txt)) | Linux, macOS | [fluidsynth.org](https://www.fluidsynth.org) |
| ALSA library | LGPL-2.1 ([text](licenses/LGPL-2.1.txt)) | Linux | [alsa-project.org](https://www.alsa-project.org) |
| Brotli | MIT | Linux, macOS | [github.com/google/brotli](https://github.com/google/brotli) |
| zlib-ng | zlib | macOS | [github.com/zlib-ng/zlib-ng](https://github.com/zlib-ng/zlib-ng) |

## Required notices

- Portions of this software are copyright © The FreeType Project (www.freetype.org). All rights reserved.
- This software is based in part on the work of the Independent JPEG Group.

## LGPL components

pygame-ce and the LGPL libraries above are bundled unmodified inside the executables. To use a modified version of any of them, build the game from source (the code is public under the MIT license) with `tools/build_exe.py` after installing your version. See the [README](README.md) for build instructions.
