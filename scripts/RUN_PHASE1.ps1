# MindMusk Phase 1 — Run from PowerShell
# Right-click this file and choose "Run with PowerShell"

$PYTHON = "C:\Users\Akshay\AppData\Local\Programs\Python\Python311-arm64\python.exe"
$SCRIPTS_SRC = $PSScriptRoot   # This folder (where this .ps1 lives)
$SCRIPTS_DST = "C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host " MindMusk Knowledge Base — Phase 1" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Step 1: Install packages
Write-Host "`n[1/5] Installing Python packages..." -ForegroundColor Yellow
& $PYTHON -m pip install anthropic pypdf python-docx python-dotenv --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "Package install failed. Check Python path." -ForegroundColor Red
    pause
    exit 1
}
Write-Host "Packages OK" -ForegroundColor Green

# Step 2: Create destination scripts folder
Write-Host "`n[2/5] Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $SCRIPTS_DST | Out-Null
& $PYTHON "$SCRIPTS_SRC\00_setup_dirs.py"

# Step 3: Copy all scripts to MindMusk/scripts/
Write-Host "`n[3/5] Copying scripts to MindMusk/scripts/..." -ForegroundColor Yellow
Copy-Item "$SCRIPTS_SRC\*.py" -Destination $SCRIPTS_DST -Force
Write-Host "Scripts copied." -ForegroundColor Green

# Step 4: Run Phase 1A (PDF extraction — fast, no API)
Write-Host "`n[4/5] Running Phase 1A: Book PDF Extraction..." -ForegroundColor Yellow
Write-Host "This extracts text from all 41 PDFs. Takes 2-5 minutes." -ForegroundColor Gray
& $PYTHON "$SCRIPTS_DST\01_extract_books.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Phase 1A failed. Check errors above." -ForegroundColor Red
    pause
    exit 1
}
Write-Host "Phase 1A DONE" -ForegroundColor Green

# Step 5: Run Phase 1B Step 1 (Parse podcast docx)
Write-Host "`n[5/5] Running Phase 1B Step 1: Parsing Podcast Files..." -ForegroundColor Yellow
& $PYTHON "$SCRIPTS_DST\02_parse_podcasts.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Phase 1B Step 1 failed. Check errors above." -ForegroundColor Red
    pause
    exit 1
}
Write-Host "Phase 1B Step 1 DONE" -ForegroundColor Green

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host " Phase 1A + 1B-Step1 COMPLETE" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: Run RUN_PHASE1B_FILTER.ps1" -ForegroundColor Yellow
Write-Host "(This calls the Claude API — takes 1-2 hours for ~55 transcripts)" -ForegroundColor Gray
Write-Host ""
pause
