@echo off
title Real Estate Lead Engine - Data Refresh
echo ========================================
echo Refreshing Real Estate Lead Data
echo ========================================
echo.

cd /d "C:\Users\NEECA\PycharmProjects\real_estate_lead_engine"

echo [1/5] Running scraper...
call .venv\Scripts\python main.py

echo.
echo [2/5] Exporting data for web...
call .venv\Scripts\python scripts\export_for_web.py

echo.
echo [3/5] Stashing local changes...
git stash

echo.
echo [4/5] Pulling latest from GitHub...
git pull origin main

echo.
echo [5/5] Applying changes and pushing...
git stash pop
git add data/ docs/
git commit -m "Auto-update leads data - %date% %time%"
git push origin main

echo.
echo ========================================
echo ✅ Data refresh complete!
echo ========================================
pause