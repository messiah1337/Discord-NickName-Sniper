@echo off
cls
echo Installing 'aiohttp' module...
python -m pip install aiohttp

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to install 'aiohttp' module. Make sure Python and pip are properly installed.
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCESS] 'aiohttp' module has been installed successfully!
    timeout /t 2 >nul
)
exit