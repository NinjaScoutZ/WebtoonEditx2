@echo off
chcp 65001 >nul
cd /d "%~dp0"

set ERROR_REPORTING=FALSE

mkdir tmp 2>NUL

@REM ใช้ Python จากระบบ (python.exe หรือ py)
where python.exe >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PYTHON=python.exe
    goto :check_pip
)

where py >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PYTHON=py
    goto :check_pip
)

echo Error: Python not found. Please install Python 3.10 or higher.
pause
exit /b 1

:check_pip
%PYTHON% -mpip --help >tmp/stdout.txt 2>tmp/stderr.txt
if %ERRORLEVEL% == 0 goto :launch
echo Couldn't find pip. Please install pip.
goto :show_stdout_stderr

:launch
echo Launching with: %PYTHON%
%PYTHON% launch.py %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Exit code: %ERRORLEVEL%
    pause
)
exit /b

:show_stdout_stderr
echo.
echo exit code: %errorlevel%

for /f %%i in ("tmp\stdout.txt") do set size=%%~zi
if %size% equ 0 goto :show_stderr
echo.
echo stdout:
type tmp\stdout.txt

:show_stderr
for /f %%i in ("tmp\stderr.txt") do set size=%%~zi
if %size% equ 0 goto :end
echo.
echo stderr:
type tmp\stderr.txt

:end
echo.
echo Launch unsuccessful. Exiting.
pause
