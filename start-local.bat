@echo off
cd /d "c:\Users\Propietario\Documents\tareasDjango"

echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

echo 📦 Aplicando migraciones...
python manage.py migrate

echo 👤 Creando superusuario (si no existe)...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@mediafind.com', 'admin123')"

echo 📝 Poblando base de datos...
python populate_db.py

echo 🌐 Iniciando servidor...
echo Accede a: http://localhost:8000
echo Usuario: admin
echo Contraseña: admin123
python manage.py runserver
