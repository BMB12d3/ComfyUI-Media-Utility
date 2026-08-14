# ComfyUI Media Utility

A lightweight local media companion for ComfyUI workflows.

**Extract / Trim · Sort · Compare**

The goal is simple: handle the quick media jobs that do not justify opening a full Premiere, Audition, Resolve, or other editing project.

> This project is a standalone companion utility. It is not a ComfyUI custom node and is not affiliated with the ComfyUI project.

## Screenshots

### Extract / Trim

![Extract / Trim](docs/screenshots/extract-trim.png)

### Sort

![Sort](docs/screenshots/sort.png)

### Compare

![Compare](docs/screenshots/compare.png)

For step-by-step instructions, see the **[Full User Guide](docs/USER_GUIDE.md)**.

## What it does

### Extract / Trim
- Drag/drop or choose video and audio files.
- Full-clip and precision **zoomed timeline** scrubbing.
- High-visibility overview of the active zoom window.
- Lock the zoomed timeline range while scrubbing.
- **Center on Playhead** and **Playhead → Left** timeline navigation.
- Set **In / Out** points.
- Play only the selected range.
- Full-resolution PNG frame grabs.
- Mouse-wheel image zoom and click-drag pan for close inspection.
- Export selected audio as uncompressed **48 kHz WAV**.
- Export selected video as:
  - **Fast Cut** — stream copy / no recompression when compatible.
  - **Exact Cut** — H.264/AAC re-encode for more precise edit points.
- Choose an output folder or use normal browser downloads.

### Sort
- Sort **images, videos, and audio** from a source folder into category folders.
- Move or Copy modes.
- Destination-folder hotkeys.
- Autoplay previews for video/audio.
- Filters for All / Images / Videos / Audio.
- Skip, Back, Trash, and Undo.
- Drag/drop folder setup.

### Compare
- Side-by-side comparison for **images, videos, and audio**.
- Tournament and Browse modes.
- Optional **Reference** image/video/audio in the center.
- Adjustable Reference panel size.
- Shortlist / finalists / winner workflow.
- Copy or move winners/shortlists to a destination.
- Mouse-wheel zoom and click-drag pan.
- Flexible **View Sync**:
  - `Left + Right` (default)
  - `All 3`
  - `None`
- Sync **Zoom** and **Pan** independently.
- **Reset View** without clearing the comparison.
- Audio audition modes:
  - **Hover Audio** — hear whichever comparison/reference pane you hover.
  - **Select Audio** — explicitly choose Left / Reference / Right.

## Requirements

### Windows release
- Windows 10/11
- **Python 3**
- **Chrome or Edge recommended**

Python is only used for the tiny local web server and first-time FFmpeg engine setup.  
There are **no pip packages, Node.js packages, virtual environments, or ComfyUI custom nodes to install**.

Chrome/Edge is recommended because writable folder selection uses the File System Access API.

## Install / run

1. Download the Windows release ZIP.
2. Extract the entire folder somewhere.
3. Double-click:

   `Launch_ComfyUI_Media_Utility.bat`

4. Leave the small command window open while using the app.
5. The utility opens automatically in your browser.

The app is served only from:

`127.0.0.1`

That is your own computer. Your media is not uploaded to a server.

## FFmpeg setup

MP4/WAV export uses ffmpeg.wasm.

On the **first launch**, the Python launcher downloads approximately **32 MB** of FFmpeg browser-engine files and caches them under:

`vendor/ffmpeg/`

After that, those engine files are loaded locally.

The pinned versions are:

- `@ffmpeg/ffmpeg` **0.12.15**
- `@ffmpeg/core` **0.12.10**

If the download fails, the app still launches. **Sort, Compare, playback, and PNG frame capture continue to work.**  
To retry or repair the export engine, run:

`Setup_FFmpeg_Engine.bat`

### Why the FFmpeg core is downloaded instead of committed here

The JavaScript wrapper and FFmpeg core have different upstream licenses. The repository keeps third-party runtime binaries out of the project archive and downloads the pinned upstream packages on the user's machine. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Privacy

Media files are processed locally in the browser.

The utility does **not** upload your source images, video, or audio.

Network access is used only when the pinned FFmpeg engine files need to be downloaded or repaired.

## Useful shortcuts

### App
- `Alt+1` — Extract / Trim
- `Alt+2` — Sort
- `Alt+3` — Compare

### Extract / Trim
- `Space` — Play / Pause
- `← / →` — ±1 second
- `Shift + ← / →` — ±10 seconds
- `I` — Set In
- `O` — Set Out
- `C` — Capture PNG

### Compare
- `← / →` — Keep left / right in Tournament
- `Space` — Play / pause media
- `S` — Sync loops
- `1 / 2` — Shortlist left / right
- `U` — Undo
- `R` — Reference on/off
- `F` — Fullscreen
- `0` — Reset all visible views
- Mouse wheel — Zoom
- Drag — Pan

## Notes and limitations

- Browser playback support still depends on codecs supported by your browser.
- **Fast Cut** is intentionally fast and avoids recompression, but its start point can align to a nearby keyframe.
- **Exact Cut** is more precise but slower because H.264 encoding runs through WebAssembly in the browser.
- Some browser autoplay policies may require one click before audio can begin.
- Writable folder access is best in Chrome/Edge.
- Large or very long files may require more memory for exact re-encoding.

## Project layout

```text
ComfyUI-Media-Utility/
├── index.html
├── extract_trim.html
├── sort.html
├── compare.html
├── launch_media_utility.py
├── setup_ffmpeg.py
├── Launch_ComfyUI_Media_Utility.bat
├── Setup_FFmpeg_Engine.bat
├── vendor/
│   └── ffmpeg/               # populated locally on first setup
├── README.md
├── CHANGELOG.md
├── THIRD_PARTY_NOTICES.md
├── CONTRIBUTING.md
└── LICENSE
```

## Development

No build process is required for the app itself.

For local development:

```bash
python launch_media_utility.py --skip-deps
```

To test with the FFmpeg engine prepared:

```bash
python setup_ffmpeg.py
python launch_media_utility.py
```

The HTML workspaces are deliberately kept readable and dependency-light.

## License

The original project code is released under the [MIT License](LICENSE).

Third-party components retain their own licenses. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
