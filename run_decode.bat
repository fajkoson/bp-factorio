@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

:: Check if the virtual environment exists, if not, create it
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate the virtual environment
call .venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Run the decoding script within the virtual environment
python scripts\base64decode.py

:: Deactivate the virtual environment after running the script
deactivate
