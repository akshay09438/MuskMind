# MindMusk Phase 3 — 15 Thematic Syntheses
# Run AFTER Phase 2 is complete (must have 80+ files in second_order/)
# Takes 1-2 hours.

$PYTHON = "C:\Users\Akshay\AppData\Local\Programs\Python\Python311-arm64\python.exe"
$SCRIPTS_DST = "C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts"
$SECOND_ORDER = "C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\second_order"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host " MindMusk — Phase 3: Third-Order" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$so_files = (Get-ChildItem "$SECOND_ORDER\*.md" -ErrorAction SilentlyContinue).Count
Write-Host "Second-order files found: $so_files" -ForegroundColor Gray
if ($so_files -lt 80) {
    Write-Host "ERROR: Need at least 80 second-order files. Only found $so_files." -ForegroundColor Red
    Write-Host "Complete Phase 2 first." -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Starting Phase 3 — 15 thematic synthesis docs. ~1-2 hours." -ForegroundColor Gray
& $PYTHON "$SCRIPTS_DST\05_generate_third_order.py"

Write-Host "`nPhase 3 COMPLETE" -ForegroundColor Green
Write-Host "Next: Run RUN_PHASE4.ps1" -ForegroundColor Yellow
pause
