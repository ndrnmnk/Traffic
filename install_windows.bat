@echo off
REM ================================================
REM Project Installer Script for Windows
REM ================================================

echo Checking for Python installation...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo "Python3 not found. Please install it from https://www.python.org/downloads/ and try again."
    pause
    exit /b 1
)

REM Set project venv folder name
set VENV_DIR=venv

REM Create virtual environment if it does not exist
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
) else (
    echo Virtual environment already exists, skipping creation.
)

REM Activate venv and install requirements
echo Installing requirements...
call %VENV_DIR%\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
deactivate

REM Create launcher script
set LAUNCHER=launch.bat
echo Creating launch script...

(
echo @echo off
echo call %%~dp0%VENV_DIR%\Scripts\activate.bat
echo python %%~dp0main.py %%*
) > %LAUNCHER%

echo Setup complete! Use %LAUNCHER% to run the project.
pause
