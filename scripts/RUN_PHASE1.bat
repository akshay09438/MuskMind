@echo off
SET PYTHON=C:\Users\Akshay\AppData\Local\Programs\Python\Python311-arm64\python.exe
SET SCRIPTS_SRC=%~dp0
SET SCRIPTS_DST=C:\Users\Akshay\OneDrive\Desktop\MindMusk\scripts

echo ======================================
echo  MindMusk Knowledge Base - Phase 1
echo ======================================

echo.
echo [1/5] Installing Python packages...
"%PYTHON%" -m pip install anthropic pypdf python-docx python-dotenv
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Package install failed. Check Python path.
    pause
    exit /b 1
)
echo Packages OK

echo.
echo [2/5] Creating directories...
if not exist "%SCRIPTS_DST%" mkdir "%SCRIPTS_DST%"
"%PYTHON%" "%SCRIPTS_SRC%00_setup_dirs.py"

echo.
echo [3/5] Copying scripts to MindMusk/scripts/...
copy "%SCRIPTS_SRC%*.py" "%SCRIPTS_DST%\" /Y
echo Scripts copied.

echo.
echo [4/5] Running Phase 1A: Book PDF Extraction...
echo This extracts text from all 41 PDFs. Takes 2-5 minutes.
"%PYTHON%" "%SCRIPTS_DST%\01_extract_books.py"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Phase 1A failed.
    pause
    exit /b 1
)
echo Phase 1A DONE

echo.
echo [5/5] Running Phase 1B Step 1: Parsing Podcast Files...
"%PYTHON%" "%SCRIPTS_DST%\02_parse_podcasts.py"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Phase 1B Step 1 failed.
    pause
    exit /b 1
)
echo Phase 1B Step 1 DONE

echo.
echo ======================================
echo  Phase 1A + 1B-Step1 COMPLETE
echo ======================================
echo.
echo Next step: Run RUN_PHASE1B_FILTER.bat
echo (Calls Claude API - takes 1-2 hours for ~55 transcripts)
echo.
pause
