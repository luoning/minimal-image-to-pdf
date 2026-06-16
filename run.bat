@echo off
title PDF Lossless Compression and Merging Service

echo ============================================================
echo      PDF Lossless Compression and Merging Service (CLI)
echo ============================================================
echo.

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in system PATH. Please install Python first.
    pause
    exit /b
)

:: Get target folder from drag-and-drop or prompt
set "TARGET_FOLDER=%~1"
set "INPUT_PATH="

if "%TARGET_FOLDER%"=="" (
    echo [TIP] You can drag and drop a folder onto this bat file to convert it.
    echo.
    set /p "INPUT_PATH=Please enter image folder path [Press Enter for default .raw\20260616]: "
)

if "%INPUT_PATH%"=="" (
    if "%TARGET_FOLDER%"=="" (
        set "TARGET_FOLDER=%~dp0.raw\20260616"
    )
) else (
    set "TARGET_FOLDER=%INPUT_PATH%"
)

:: Remove quotes from path
set "TARGET_FOLDER=%TARGET_FOLDER:"=%"

echo.
echo Starting PDF conversion...
echo Target Folder: "%TARGET_FOLDER%"
echo.

python "%~dp0app.py" -f "%TARGET_FOLDER%"

echo.
echo ============================================================
pause
