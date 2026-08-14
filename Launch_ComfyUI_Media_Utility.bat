@echo off
setlocal
cd /d "%~dp0"
title ComfyUI Media Utility v1.0.0

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py -3 launch_media_utility.py
    goto :eof
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
    python launch_media_utility.py
    goto :eof
)

echo.
echo Python 3 was not found.
echo.
echo ComfyUI Media Utility needs Python 3 only to run its local-only web server
echo and prepare the FFmpeg browser engine. No pip packages are required.
echo.
pause
