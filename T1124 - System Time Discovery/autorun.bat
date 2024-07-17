@echo off
echo Installing required Python packages...
pip install --user firebase-admin
if %errorlevel% neq 0 (
    echo Failed to install firebase-admin. Please check your internet connection and try again.
    pause
    exit /b 1
)
echo Running the Python script...
python log_system_time.py
pause
