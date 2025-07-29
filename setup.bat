@echo off
cls
echo Running index.py...

:: index.py çalıştır ve hataları logla
python index.py 2>index_error.log

:: index.py modül hatası kontrolü
findstr /C:"ModuleNotFoundError" index_error.log >nul
if %errorlevel% equ 0 (
    echo.
    echo [index.py] Missing module detected:

    for /f "tokens=*" %%i in ('findstr /C:"ModuleNotFoundError" index_error.log') do (
        set "line=%%i"
    )
    for /f "tokens=2 delims=''" %%m in ("%line%") do (
        set "missing_module=%%m"
    )

    echo Trying to install module: %missing_module%
    pip install %missing_module%

    echo.
    echo Re-running index.py...
    python index.py
) else (
    if exist index_error.log (
        findstr . index_error.log >nul
        if %errorlevel% equ 0 (
            echo.
            echo [index.py] An error occurred:
            type index_error.log
        ) else (
            echo.
            echo index.py executed successfully.
        )
    )
)

echo.
echo -------------------------------------
echo Running asd.py...

:: asd.py çalıştır ve hataları logla
python asd.py 2>asd_error.log

:: asd.py modül hatası kontrolü
findstr /C:"ModuleNotFoundError" asd_error.log >nul
if %errorlevel% equ 0 (
    echo.
    echo [asd.py] Missing module detected:

    for /f "tokens=*" %%i in ('findstr /C:"ModuleNotFoundError" asd_error.log') do (
        set "line=%%i"
    )
    for /f "tokens=2 delims=''" %%m in ("%line%") do (
        set "missing_module=%%m"
    )

    echo Trying to install module: %missing_module%
    pip install %missing_module%

    echo.
    echo Re-running asd.py...
    python asd.py
) else (
    if exist asd_error.log (
        findstr . asd_error.log >nul
        if %errorlevel% equ 0 (
            echo.
            echo [asd.py] An error occurred:
            type asd_error.log
        ) else (
            echo.
            echo asd.py executed successfully.
        )
    )
)

echo.
pause