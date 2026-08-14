@echo off
setlocal
cd /d "%~dp0"
title ComfyUI Media Utility - FFmpeg Setup

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py -3 setup_ffmpeg.py --force
    goto :done
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
    python setup_ffmpeg.py --force
    goto :done
)

echo.
echo Python 3 was not found.
goto :done

:done
echo.
pause
