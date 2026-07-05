@echo off
cd /d "C:\Users\Akshay\OneDrive\Desktop\MindMusk"
python extract_pdf.py > extract_log.txt 2>&1
echo Script completed. Check extract_log.txt for details.
pause
