@echo off
title Real Estate Lead Engine - Daily Run
echo ========================================
echo Real Estate Lead Engine
echo Daily Automated Run
echo ========================================
echo.

cd /d "C:\Users\NEECA\PycharmProjects\real_estate_lead_engine"

echo [%date% %time%] Starting pipeline...
call .venv\Scripts\python main.py

echo [%date% %time%] Exporting data for web...
call .venv\Scripts\python scripts\export_for_web.py

echo [%date% %time%] Uploading to GitHub...
git add docs/ data/leads_data.json
git commit -m "Daily update: %date% %time%"
git push origin main

echo [%date% %time%] Pipeline completed!
echo.
pause