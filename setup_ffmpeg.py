#!/usr/bin/env python3
"""
Download and cache the browser FFmpeg engine used by Extract / Trim.

No pip packages are required. Files are stored under vendor/ffmpeg/ and are
loaded only from localhost by the app after setup.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

FFMPEG_WRAPPER_VERSION = "0.12.15"
FFMPEG_CORE_VERSION = "0.12.10"

ROOT = Path(__file__).resolve().parent
VENDOR = ROOT / "vendor" / "ffmpeg"

FILES = [
    {
        "rel": "ffmpeg/classes.js",
        "min_size": 7000,
        "urls": [
            f"https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/classes.js",
            f"https://unpkg.com/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/classes.js",
        ],
    },
    {
        "rel": "ffmpeg/const.js",
        "min_size": 700,
        "urls": [
            f"https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/const.js",
            f"https://unpkg.com/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/const.js",
        ],
    },
    {
        "rel": "ffmpeg/errors.js",
        "min_size": 200,
        "urls": [
            f"https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/errors.js",
            f"https://unpkg.com/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/errors.js",
        ],
    },
    {
        "rel": "ffmpeg/utils.js",
        "min_size": 100,
        "urls": [
            f"https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/utils.js",
            f"https://unpkg.com/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/utils.js",
        ],
    },
    {
        "rel": "ffmpeg/worker.js",
        "min_size": 3000,
        "urls": [
            f"https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/worker.js",
            f"https://unpkg.com/@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}/dist/esm/worker.js",
        ],
    },
    {
        "rel": "core/ffmpeg-core.js",
        "min_size": 80000,
        "urls": [
            f"https://cdn.jsdelivr.net/npm/@ffmpeg/core@{FFMPEG_CORE_VERSION}/dist/esm/ffmpeg-core.js",
            f"https://unpkg.com/@ffmpeg/core@{FFMPEG_CORE_VERSION}/dist/esm/ffmpeg-core.js",
        ],
    },
    {
        "rel": "core/ffmpeg-core.wasm",
        "min_size": 30_000_000,
        "urls": [
            f"https://cdn.jsdelivr.net/npm/@ffmpeg/core@{FFMPEG_CORE_VERSION}/dist/esm/ffmpeg-core.wasm",
            f"https://unpkg.com/@ffmpeg/core@{FFMPEG_CORE_VERSION}/dist/esm/ffmpeg-core.wasm",
        ],
    },
]

USER_AGENT = "ComfyUI-Media-Utility/1.0.0 (+GitHub release)"


def valid(path: Path, min_size: int) -> bool:
    try:
        return path.is_file() and path.stat().st_size >= min_size
    except OSError:
        return False


def _download(url: str, dest: Path, min_size: int, quiet: bool = False) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    tmp = dest.with_suffix(dest.suffix + ".part")
    if tmp.exists():
        tmp.unlink()

    try:
        with urllib.request.urlopen(req, timeout=45) as response, open(tmp, "wb") as out:
            total = int(response.headers.get("Content-Length") or 0)
            received = 0
            last_mb = -1
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
                received += len(chunk)
                if not quiet and total >= 5_000_000:
                    mb = received // (5 * 1024 * 1024)
                    if mb != last_mb:
                        last_mb = mb
                        pct = (received / total * 100) if total else 0
                        print(f"      {received/1024/1024:5.1f} MB"
                              + (f" / {total/1024/1024:.1f} MB ({pct:3.0f}%)" if total else ""))
        if not valid(tmp, min_size):
            size = tmp.stat().st_size if tmp.exists() else 0
            raise RuntimeError(f"downloaded file is unexpectedly small ({size} bytes)")
        os.replace(tmp, dest)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def ensure_dependencies(force: bool = False, quiet: bool = False) -> bool:
    VENDOR.mkdir(parents=True, exist_ok=True)
    missing = [spec for spec in FILES if force or not valid(VENDOR / spec["rel"], spec["min_size"])]

    if not missing:
        if not quiet:
            print("FFmpeg engine: ready (local cache)")
        return True

    if not quiet:
        print()
        print("Preparing FFmpeg browser engine")
        print("--------------------------------")
        print("This is a one-time download of about 32 MB.")
        print("The files are cached locally under vendor/ffmpeg/.")
        print()

    failures = []
    for spec in missing:
        dest = VENDOR / spec["rel"]
        if not quiet:
            print(f"  {spec['rel']}")
        last_error = None
        for url in spec["urls"]:
            try:
                _download(url, dest, spec["min_size"], quiet=quiet)
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                if not quiet:
                    print(f"    source failed: {exc}")
        if last_error is not None:
            failures.append((spec["rel"], str(last_error)))

    if failures:
        if not quiet:
            print()
            print("FFmpeg engine setup was incomplete:")
            for name, err in failures:
                print(f"  - {name}: {err}")
        return False

    manifest = {
        "wrapper": f"@ffmpeg/ffmpeg@{FFMPEG_WRAPPER_VERSION}",
        "core": f"@ffmpeg/core@{FFMPEG_CORE_VERSION}",
        "files": [spec["rel"] for spec in FILES],
    }
    (VENDOR / "installed.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if not quiet:
        print()
        print("FFmpeg engine: ready.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare the local FFmpeg browser engine.")
    parser.add_argument("--force", action="store_true", help="redownload all FFmpeg files")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    ok = ensure_dependencies(force=args.force, quiet=args.quiet)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
