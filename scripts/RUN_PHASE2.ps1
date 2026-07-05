# MindMusk Phase 2 — Second-Order Elon Syntheses
# Run AFTER Phase 1 is complete (must have 80+ files in first_order/)
# WARNING: Makes ~96 Claude API calls with map-reduce for large books.
# Takes 4-8 hours. Safe to interrupt and restart.

$PYTHON = "C:\Users\Akshay\AppData\Local\Programs\Python\Python311-arm64\python.exe"
$SCRIPTS_DST = "C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts"
$FIRST_ORDER = "C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\first_order"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host " MindMusk — Phase 2: Second-Order" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Check Phase 1 is done
$fo_files = (Get-ChildItem "$FIRST_ORDER\*.md" -ErrorAction SilentlyContinue).Count
Write-Host "First-order files found: $fo_files" -ForegroundColor Gray
if ($fo_files -lt 80) {
    Write-Host "ERROR: Need at least 80 first-order files. Only found $fo_files." -ForegroundColor Red
    Write-Host "Complete Phase 1 first." -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Starting Phase 2 — this takes 4-8 hours. Safe to restart." -ForegroundColor Gray
& $PYTHON "$SCRIPTS_DST\04_generate_second_order.py"

Write-Host "`nPhase 2 COMPLETE" -ForegroundColor Green
Write-Host "Next: Run RUN_PHASE3.ps1" -ForegroundColor Yellow
pause
