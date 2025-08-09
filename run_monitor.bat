@echo off
echo Ubuntu Repository Monitor
echo ========================
echo.
echo Options:
echo 1. Run once (single check)
echo 2. Run continuously (every 30 minutes)
echo 3. Run continuously (custom interval)
echo 4. Exit
echo.

set /p choice=Enter your choice (1-4): 

if "%choice%"=="1" (
    echo Running single check...
    python ubuntu_repo_monitor.py --once
    pause
) else if "%choice%"=="2" (
    echo Starting continuous monitoring (30 min intervals)...
    python ubuntu_repo_monitor.py 30
) else if "%choice%"=="3" (
    set /p interval=Enter interval in minutes: 
    echo Starting continuous monitoring (%interval% min intervals)...
    python ubuntu_repo_monitor.py %interval%
) else if "%choice%"=="4" (
    exit
) else (
    echo Invalid choice!
    pause
)
