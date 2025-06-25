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
    echo ⚠️ Problema de conectividad con Docker Hub. Intentando con imagen local...
    goto DOCKER_SIMPLE
)

echo 🐳 Ejecutando con Docker Compose completo...
docker-compose down
docker-compose up --build -d
goto SUCCESS

:DOCKER_SIMPLE
echo 🐳 Usando Dockerfile simplificado...
docker build -f Dockerfile.simple -t mediafind-simple .
if errorlevel 1 (
    echo ❌ Error building imagen. Ejecutando en modo local...
    goto LOCAL_MODE
)
docker run -d -p 8000:8000 --name mediafind-app mediafind-simple
goto SUCCESS

:LOCAL_MODE
echo 🖥️ Ejecutando en modo local con Python...
if not exist "venv\Scripts\python.exe" (
    echo ❌ Entorno virtual no encontrado. Creando uno nuevo...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo � Ejecutando migraciones...
python manage.py migrate

echo 👤 Creando superusuario...
echo from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mediafind.com', 'admin123') | python manage.py shell

echo � Poblando base de datos...
python populate_db.py

echo 🌐 Iniciando servidor...
start "MediaFind Server" python manage.py runserver
goto LOCAL_SUCCESS

:SUCCESS
echo ⏳ Esperando a que los servicios estén listos...
timeout /t 10 /nobreak > nul
echo 🎉 ¡MediaFind está ejecutándose en Docker!
goto END

:LOCAL_SUCCESS
echo 🎉 ¡MediaFind está ejecutándose localmente!

:END
echo.
echo 📍 Accede a: http://localhost:8000
echo 👤 Usuario admin: admin
echo 🔑 Contraseña: admin123
echo.
pause
