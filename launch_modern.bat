@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   Modern Manga Translator
echo   Version 2.0.0
echo ========================================
echo.

set ERROR_REPORTING=FALSE

mkdir tmp 2>NUL
mkdir logs 2>NUL

@REM Find Python
where python.exe >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PYTHON=python.exe
    goto :launch
)

where py >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PYTHON=py
    goto :launch
)

echo [ERROR] Python not found!
echo Please install Python 3.10 or higher.
pause
exit /b 1

:launch
echo [INFO] Python found: %PYTHON%
echo [INFO] Starting Modern Manga Translator...
echo.

%PYTHON% launch_modern.py %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application exited with code: %ERRORLEVEL%
    pause
)

exit /b
