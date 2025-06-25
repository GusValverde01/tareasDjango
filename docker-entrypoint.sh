#!/bin/bash

# Script de entrada para Docker
set -e

echo "🚀 Iniciando MediaFind..."

# Esperar a que la base de datos esté disponible (solo si se usa PostgreSQL)
if [ "$DATABASE_URL" ]; then
    echo "⏳ Esperando a que PostgreSQL esté disponible..."
    
    # Extraer información de la URL de la base de datos
    DB_HOST=$(echo $DATABASE_URL | sed 's/.*@\([^:]*\):.*/\1/')
    DB_PORT=$(echo $DATABASE_URL | sed 's/.*:\([0-9]*\)\/.*/\1/')
    
    # Esperar hasta que PostgreSQL esté disponible
    while ! nc -z $DB_HOST $DB_PORT; do
        echo "🔄 PostgreSQL no disponible en $DB_HOST:$DB_PORT, esperando..."
        sleep 1
    done
    
    echo "✅ PostgreSQL disponible!"
fi

# Ejecutar migraciones
echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

# Crear superusuario si no existe
echo "👤 Verificando superusuario..."
python manage.py shell << END
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@mediafind.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superusuario '{username}' creado")
else:
    print(f"ℹ️ Superusuario '{username}' ya existe")
END

# Poblar base de datos con datos de ejemplo si está vacía
echo "🗃️ Verificando datos de ejemplo..."
python manage.py shell << END
from tasks.models import ContentItem, Genre, Category
import os

# Solo poblar si la base de datos está vacía
if ContentItem.objects.count() == 0 and os.environ.get('POPULATE_DB', 'true').lower() == 'true':
    print("📝 Poblando base de datos con datos de ejemplo...")
    exec(open('populate_db.py').read())
    print("✅ Base de datos poblada con datos de ejemplo")
else:
    print("ℹ️ Base de datos ya contiene datos")
END

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "🎉 MediaFind listo para usar!"
echo "📍 Accede a: http://localhost:8000"
echo "👤 Usuario admin: admin"
echo "🔑 Contraseña: admin123"

# Ejecutar comando pasado como argumentos
exec "$@"
