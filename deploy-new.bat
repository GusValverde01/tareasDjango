@echo off
echo 🚀 Desplegando MediaFind...

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está instalado. Ejecutando en modo local...
    goto LOCAL_MODE
)

echo 🔍 Verificando conectividad con Docker Hub...
ping -n 1 auth.docker.io >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Problema de conectividad con Docker Hub.
    echo 🤔 ¿Quieres intentar con Docker local (SQLite) o modo local? 
    echo [1] Docker con SQLite (Recomendado si Docker funciona)
    echo [2] Modo local con Python
    set /p choice="Selecciona una opción (1 o 2): "
    
    if "%choice%"=="1" goto DOCKER_SQLITE
    if "%choice%"=="2" goto LOCAL_MODE
    goto DOCKER_SQLITE
)

echo 🐳 Intentando Docker Compose completo con PostgreSQL...
docker-compose down
docker-compose up --build -d

echo ⏳ Esperando 15 segundos para que los servicios se inicialicen...
timeout /t 15 /nobreak > nul

echo 📊 Verificando estado de los servicios...
docker-compose ps

REM Verificar si el servicio web está funcionando
docker-compose logs web | findstr "Error\|error\|Exception" >nul
if not errorlevel 1 (
    echo ⚠️ Se detectaron errores en el contenedor web. Intentando con SQLite...
    docker-compose down
    goto DOCKER_SQLITE
)

goto SUCCESS

:DOCKER_SQLITE
echo 🐳 Usando Docker con SQLite (más simple y confiable)...
docker-compose -f docker-compose.local.yml down
docker-compose -f docker-compose.local.yml up --build -d
if errorlevel 1 (
    echo ❌ Error con Docker SQLite. Ejecutando en modo local...
    goto LOCAL_MODE
)
goto SUCCESS

:LOCAL_MODE
echo 🖥️ Ejecutando en modo local con Python...
if not exist "venv\Scripts\python.exe" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual. Verifica que Python esté instalado.
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
    echo 📥 Instalando dependencias...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo 📦 Ejecutando migraciones...
python manage.py migrate

echo 👤 Verificando superusuario...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mediafind.com', 'admin123')" 2>nul

echo 📝 Poblando base de datos...
python populate_db.py 2>nul

echo 🌐 Iniciando servidor local...
echo.
echo ✅ Servidor iniciándose...
echo 📍 Accediendo automáticamente a: http://localhost:8000
start http://localhost:8000
python manage.py runserver
goto END

:SUCCESS
echo ⏳ Esperando a que los servicios estén completamente listos...
timeout /t 10 /nobreak > nul

echo 📍 Accediendo automáticamente a: http://localhost:8000
start http://localhost:8000

echo 🎉 ¡MediaFind está ejecutándose en Docker!

:END
echo.
echo 📍 URL: http://localhost:8000
echo 👤 Usuario admin: admin
echo 🔑 Contraseña: admin123
echo.
echo 📝 Comandos útiles:
echo    Ver logs Docker: docker-compose logs -f web
echo    Parar Docker: docker-compose down
echo    Reiniciar: docker-compose restart
echo.
pause
