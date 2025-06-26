#!/bin/bash

# Script de entrada para Docker
set -e

echo "🚀 Iniciando MediaFind..."

# Función para esperar a PostgreSQL
wait_for_postgres() {
    local host=$1
    local port=$2
    local max_attempts=60  # 60 intentos = 5 minutos máximo
    local attempt=1
    
    echo "⏳ Esperando a que PostgreSQL esté disponible en $host:$port..."
    
    while [ $attempt -le $max_attempts ]; do
        if nc -z $host $port 2>/dev/null; then
            echo "✅ PostgreSQL disponible!"
            # Esperar un poco más para asegurar que la DB esté completamente inicializada
            sleep 10
            return 0
        fi
        
        echo "🔄 Intento $attempt/$max_attempts - PostgreSQL no disponible, esperando..."
        sleep 5
        attempt=$((attempt + 1))
    done
    
    echo "❌ Error: PostgreSQL no disponible después de $max_attempts intentos"
    return 1
}

# Esperar a que la base de datos esté disponible (solo si se usa PostgreSQL)
if [ "$DATABASE_URL" ]; then
    # Extraer información de la URL de la base de datos
    DB_HOST=$(echo $DATABASE_URL | sed 's/.*@\([^:]*\):.*/\1/')
    DB_PORT=$(echo $DATABASE_URL | sed 's/.*:\([0-9]*\)\/.*/\1/')
    
    if ! wait_for_postgres $DB_HOST $DB_PORT; then
        echo "❌ No se pudo conectar a PostgreSQL. Saliendo..."
        exit 1
    fi
    
    # Verificar conexión a la base de datos con reintentos
    echo "🔗 Verificando conexión a la base de datos..."
    max_db_attempts=10
    db_attempt=1
    
    while [ $db_attempt -le $max_db_attempts ]; do
        if python manage.py check --database default >/dev/null 2>&1; then
            echo "✅ Conexión a la base de datos verificada!"
            break
        fi
        
        echo "🔄 Intento $db_attempt/$max_db_attempts - Verificando conexión DB..."
        sleep 3
        db_attempt=$((db_attempt + 1))
    done
    
    if [ $db_attempt -gt $max_db_attempts ]; then
        echo "❌ Error: No se pudo verificar la conexión a la base de datos"
        exit 1
    fi
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
