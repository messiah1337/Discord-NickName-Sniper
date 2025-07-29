@echo off
setlocal

:: Python 3.12.0 x64 installer URL
set "PYTHON_URL=https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
set "INSTALLER=%TEMP%\python-3.12.0-amd64.exe"

:: Python indiriliyor...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER%'"

:: Python sessiz kurulum başlatılıyor...
:: Açıklama:
:: /quiet = hiçbir pencere olmadan kur
:: InstallAllUsers=1 = tüm kullanıcılar için kur
:: PrependPath=1 = PATH'e ekle
:: Include_test=0 = test modüllerini kurma
:: Include_launcher=1 = Python launcher'ı kur
:: SimpleInstall=1 = tüm seçenekleri default yap
:: Shortcuts=0 = masaüstü kısayolu kurma (isteğe bağlı)

"%INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_launcher=1 SimpleInstall=1 Shortcuts=0

:: Temizlik
del "%INSTALLER%"

endlocal
exit