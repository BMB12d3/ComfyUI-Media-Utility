# Contributing

Contributions and bug reports are welcome.

## Development setup

There is no frontend build step.

```bash
python launch_media_utility.py --skip-deps
```

For MP4/WAV export testing:

```bash
python setup_ffmpeg.py
python launch_media_utility.py
```

## Pull requests

Please:
- Keep the utility lightweight and local-first.
- Avoid adding cloud upload requirements.
- Preserve drag/drop and keyboard-driven workflows.
- Test Chrome/Edge on Windows when changing folder-access behavior.
- Run JavaScript syntax checks on all HTML workspaces.
- Describe user-facing changes in `CHANGELOG.md`.

## Bug reports

Useful information includes:
- Windows version
- Browser and version
- Python version
- Which workspace is affected: Extract / Trim, Sort, or Compare
- Media format / codec if relevant
- Console error text when available
