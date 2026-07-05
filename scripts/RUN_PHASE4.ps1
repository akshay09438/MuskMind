# MindMusk Phase 4 — 5 Master Mental Model Documents
# Run AFTER Phase 3 is complete (must have all 15 third-order files)
# Takes ~30-60 minutes.

$PYTHON = "C:\Users\Akshay\AppData\Local\Programs\Python\Python311-arm64\python.exe"
$SCRIPTS_DST = "C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts"
$THIRD_ORDER = "C:\Users\Akshay\OneDrive\Desktop\MindMusk\knowledge_base\third_order"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host " MindMusk — Phase 4: Fourth-Order" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$to_files = (Get-ChildItem "$THIRD_ORDER\*.md" -ErrorAction SilentlyContinue).Count
Write-Host "Third-order files found: $to_files" -ForegroundColor Gray
if ($to_files -lt 15) {
    Write-Host "ERROR: Need 15 third-order files. Only found $to_files." -ForegroundColor Red
    Write-Host "Complete Phase 3 first." -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Starting Phase 4 — 5 master mental model docs. ~30-60 minutes." -ForegroundColor Gray
& $PYTHON "$SCRIPTS_DST\06_generate_fourth_order.py"

Write-Host "`nPhase 4 COMPLETE" -ForegroundColor Green
Write-Host "Running final verification..." -ForegroundColor Yellow
& $PYTHON "$SCRIPTS_DST\07_verify.py"
pause
