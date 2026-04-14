@echo off
SETLOCAL ENABLEEXTENSIONS

:: 1. Changed variable name to avoid breaking the system %PATH%
set "WINRAR_EXE=C:\Program Files\WinRAR\winrar.exe"

:: 2. %~dp0 automatically gets the exact folder path where this script is running
set "ROOT_DIR=%~dp0"

:: 3. Used "delims=" to ensure file paths with spaces don't break the loop
for /F "delims=" %%f in ('dir *.zip /B /S') do (
    
    :: 4. Replaced the destination with %ROOT_DIR%
    "%WINRAR_EXE%" x -or -ilog"%ROOT_DIR%myLog.txt" "%%f" "%ROOT_DIR%"
    
    del "%%f"
)