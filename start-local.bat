@echo off
cd /d "c:\Users\Propietario\Documents\tareasDjango"

echo � Iniciando MediaFind en modo local...
echo.

REM Verificar si Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en PATH
    echo 📥 Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

echo �🔧 Activando entorno virtual...
if not exist "venv\Scripts\activate.bat" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

echo � Verificando dependencias...
pip install -r requirements.txt --quiet

echo �📦 Aplicando migraciones...
python manage.py migrate

echo 👤 Verificando superusuario (admin/admin123)...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mediafind.com', 'admin123')" 2>nul

echo 📝 Poblando base de datos con ejemplos...
python populate_db.py 2>nul

echo.
echo ✅ Todo listo! Iniciando servidor...
echo 📍 Accediendo automáticamente a: http://localhost:8000
echo 👤 Usuario: admin
echo 🔑 Contraseña: admin123
echo.

REM Abrir navegador automáticamente
start http://localhost:8000

echo 🌐 Servidor Django iniciando...
python manage.py runserver
