#!/usr/bin/env pwsh
# Ubuntu Repository Monitor - PowerShell Launcher

param(
    [string]$Action = "menu",
    [int]$Interval = 30
)

function Show-Menu {
    Clear-Host
    Write-Host "Ubuntu Repository Monitor" -ForegroundColor Cyan
    Write-Host "========================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "1. Run once (single check)" -ForegroundColor White
    Write-Host "2. Run continuously (every 30 minutes)" -ForegroundColor White
    Write-Host "3. Run continuously (custom interval)" -ForegroundColor White
    Write-Host "4. View recent logs" -ForegroundColor White
    Write-Host "5. Exit" -ForegroundColor White
    Write-Host ""
}

function Show-RecentLogs {
    Write-Host "Recent Update Summary:" -ForegroundColor Green
    Write-Host "=====================" -ForegroundColor Green
    
    if (Test-Path "logs\update_summary.log") {
        Get-Content "logs\update_summary.log" | Select-Object -Last 10
    } else {
        Write-Host "No logs found yet. Run a check first!" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "Individual repository logs available in:" -ForegroundColor Cyan
    Write-Host "  - logs\noble-main_updates.log" -ForegroundColor White
    Write-Host "  - logs\noble-updates_updates.log" -ForegroundColor White
    Write-Host "  - logs\noble-security_updates.log" -ForegroundColor White
}

if ($Action -eq "menu") {
    do {
        Show-Menu
        $choice = Read-Host "Enter your choice (1-5)"
        
        switch ($choice) {
            "1" {
                Write-Host "Running single check..." -ForegroundColor Green
                python ubuntu_repo_monitor.py --once
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            "2" {
                Write-Host "Starting continuous monitoring (30 min intervals)..." -ForegroundColor Green
                Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
                python ubuntu_repo_monitor.py 30
            }
            "3" {
                $customInterval = Read-Host "Enter interval in minutes"
                try {
                    $intervalNum = [int]$customInterval
                    Write-Host "Starting continuous monitoring ($intervalNum min intervals)..." -ForegroundColor Green
                    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
                    python ubuntu_repo_monitor.py $intervalNum
                } catch {
                    Write-Host "Invalid interval!" -ForegroundColor Red
                    Read-Host "Press Enter to continue"
                }
            }
            "4" {
                Clear-Host
                Show-RecentLogs
                Read-Host "Press Enter to continue"
            }
            "5" {
                Write-Host "Goodbye!" -ForegroundColor Green
                exit
            }
            default {
                Write-Host "Invalid choice!" -ForegroundColor Red
                Read-Host "Press Enter to continue"
            }
        }
    } while ($true)
} elseif ($Action -eq "once") {
    python ubuntu_repo_monitor.py --once
} elseif ($Action -eq "continuous") {
    python ubuntu_repo_monitor.py $Interval
}
