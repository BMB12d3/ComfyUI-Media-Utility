#!/usr/bin/env python3
from __future__ import annotations

import argparse
import mimetypes
import os
import threading
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from setup_ffmpeg import ensure_dependencies

APP_VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parent


class LocalHandler(SimpleHTTPRequestHandler):
    # Ensure browsers receive the MIME types required by ES modules / WebAssembly.
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".wasm": "application/wasm",
        ".json": "application/json",
    }

    def log_message(self, fmt, *args):
        pass

    def end_headers(self):
        # Keep local assets fresh while developing/updating the utility.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch ComfyUI Media Utility locally.")
    parser.add_argument("--no-browser", action="store_true", help="do not open the browser automatically")
    parser.add_argument("--skip-deps", action="store_true", help="skip FFmpeg dependency setup")
    parser.add_argument("--port", type=int, default=0, help="local port; 0 chooses a free port")
    args = parser.parse_args()

    os.chdir(ROOT)

    ffmpeg_ok = True
    if not args.skip_deps:
        try:
            ffmpeg_ok = ensure_dependencies()
        except Exception as exc:
            ffmpeg_ok = False
            print()
            print("WARNING: FFmpeg engine setup failed:", exc)

    server = ThreadingHTTPServer(("127.0.0.1", args.port), LocalHandler)
    port = server.server_address[1]
    url = f"http://127.0.0.1:{port}/index.html"

    print()
    print(f"ComfyUI Media Utility v{APP_VERSION}")
    print("---------------------------------")
    print("Local-only address:", url)
    print("Your media stays on this computer.")
    if ffmpeg_ok:
        print("FFmpeg export engine: ready")
    else:
        print("FFmpeg export engine: NOT READY")
        print("Sort, Compare, viewing, and PNG captures still work.")
        print("Run Setup_FFmpeg_Engine.bat later to repair MP4/WAV export.")
    print()
    print("Keep this window open while using the utility.")
    print("Press Ctrl+C here when finished.")
    print()

    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
