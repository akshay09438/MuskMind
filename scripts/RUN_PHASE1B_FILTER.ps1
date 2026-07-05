# MindMusk Phase 1B Filter — Claude API Podcast Filtering
# Run AFTER RUN_PHASE1.ps1 completes
# WARNING: This makes ~hundreds of Claude API calls. Takes 1-3 hours.

$PYTHON = "C:\Users\Akshay\AppData\Local\Programs\Python\Python311-arm64\python.exe"
$SCRIPTS_DST = "C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host " MindMusk — Phase 1B: Filter Podcasts" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script calls the Claude API to extract Elon's words" -ForegroundColor Gray
Write-Host "from ~55 podcast transcripts. It will take 1-3 hours." -ForegroundColor Gray
Write-Host "It is SAFE TO INTERRUPT and restart — it skips completed files." -ForegroundColor Gray
Write-Host ""

& $PYTHON "$SCRIPTS_DST\03_filter_podcasts.py"

Write-Host "`nPhase 1B COMPLETE" -ForegroundColor Green
Write-Host "Next: Run RUN_PHASE2.ps1" -ForegroundColor Yellow
pause
