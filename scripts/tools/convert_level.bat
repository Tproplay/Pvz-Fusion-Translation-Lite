@echo off
setlocal enabledelayedexpansion

:: PvZ Fusion Custom Level Converter (Drag & Drop or CLI Launcher)
:: Usage:
::   Drag & drop one or more JSON level files or folders onto this .bat file,
::   or run from cmd: convert_level.bat level.json

set "SCRIPT_DIR=%~dp0"

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_EXE=py"
    ) else (
        echo [ERROR] Python is not found in PATH. Please install Python 3.9+ to run this tool.
        pause
        exit /b 1
    )
) else (
    set "PYTHON_EXE=python"
)

if "%~1"=="" (
    "%PYTHON_EXE%" "%SCRIPT_DIR%convert_custom_level.py" --help
    echo.
    echo TIP: You can drag and drop custom level .json files or directories directly onto this .bat file!
    pause
    exit /b 0
)

"%PYTHON_EXE%" "%SCRIPT_DIR%convert_custom_level.py" %*

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Conversion exited with an error.
    pause
    exit /b %errorlevel%
)

:: If run via drag-and-drop (explorer), keep window open so user can see summary
if not defined PROMPT (
    echo.
    echo Press any key to exit...
    pause >nul
)
