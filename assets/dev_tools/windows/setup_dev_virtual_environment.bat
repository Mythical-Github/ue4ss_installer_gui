@echo off
cd /d "%~dp0"

call install_hatch.bat

cd /d "..\..\.."

hatch env create dev

exit /b
