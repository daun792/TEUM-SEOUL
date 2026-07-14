@echo off
setlocal
set "ROOT=%~dp0"
start "TeumSeoul API" cmd /k call "%ROOT%run_backend.bat"
start "TeumSeoul Web" cmd /k call "%ROOT%run_frontend.bat"
endlocal
