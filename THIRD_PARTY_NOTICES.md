# Third-Party Notices

ComfyUI Media Utility's original project code is licensed under MIT.

The optional MP4/WAV export feature uses the following third-party runtime packages.
They are **not included in this repository/release archive**. `setup_ffmpeg.py`
downloads the pinned files to the user's local `vendor/ffmpeg/` folder.

## ffmpeg.wasm JavaScript wrapper

- Package: `@ffmpeg/ffmpeg`
- Version: `0.12.15`
- Upstream: https://github.com/ffmpegwasm/ffmpeg.wasm
- Package page: https://www.npmjs.com/package/@ffmpeg/ffmpeg
- License reported by npm: MIT

## ffmpeg.wasm core

- Package: `@ffmpeg/core`
- Version: `0.12.10`
- Upstream: https://github.com/ffmpegwasm/ffmpeg.wasm
- Package page: https://www.npmjs.com/package/@ffmpeg/core
- License reported by npm for this version: GPL-2.0-or-later

The core package contains a WebAssembly build of FFmpeg and related components.
Upstream source and licensing information are available from the ffmpeg.wasm
repository and the FFmpeg project:

- https://github.com/ffmpegwasm/ffmpeg.wasm
- https://ffmpeg.org/
- https://ffmpeg.org/legal.html

Third-party components remain subject to their respective upstream licenses.
