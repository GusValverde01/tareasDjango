@echo off
echo 🔍 Verificando dependencias de MediaFind...

echo.
echo 📋 Verificando Python...
python --version 2>nul
if errorlevel 1 (
    echo ❌ Python no está instalado
    goto END
) else (
    echo ✅ Python instalado
)

echo.
echo 🐍 Verificando entorno virtual...
if exist "venv\Scripts\python.exe" (
    echo ✅ Entorno virtual encontrado
) else (
    echo ⚠️ Entorno virtual no encontrado
)

echo.
echo 🐳 Verificando Docker...
docker --version 2>nul
if errorlevel 1 (
    echo ❌ Docker no está instalado
) else (
    echo ✅ Docker instalado
)

echo.
echo 🔗 Verificando Docker Compose...
docker-compose --version 2>nul
if errorlevel 1 (
    echo ❌ Docker Compose no está instalado
) else (
    echo ✅ Docker Compose instalado
)

echo.
echo 🌐 Verificando conectividad...
ping -n 1 google.com >nul 2>&1
if errorlevel 1 (
    echo ❌ Sin conectividad a internet
) else (
    echo ✅ Conectividad a internet OK
)

echo.
echo 🔍 Verificando archivos del proyecto...
if exist "manage.py" (
    echo ✅ manage.py encontrado
) else (
    echo ❌ manage.py no encontrado
)

if exist "requirements.txt" (
    echo ✅ requirements.txt encontrado
) else (
    echo ❌ requirements.txt no encontrado
)

if exist "Dockerfile" (
    echo ✅ Dockerfile encontrado
) else (
    echo ❌ Dockerfile no encontrado
)

:END
echo.
echo 📝 Ejecuta deploy.bat para iniciar MediaFind
pause
