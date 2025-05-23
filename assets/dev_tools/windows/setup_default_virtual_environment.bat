@echo off
cd /d "%~dp0"

call install_hatch.bat

cd /d "..\..\.."

hatch env create

exit /b
