#!/bin/bash

# Script de despliegue de MediaFind
echo "🚀 Desplegando MediaFind con Docker..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor, instala Docker primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor, instala Docker Compose primero."
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "⚠️  Por favor, edita el archivo .env con tus configuraciones antes de continuar."
    echo "   Especialmente cambia SECRET_KEY y las contraseñas."
    read -p "¿Deseas continuar? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Parar contenedores existentes
echo "🛑 Parando contenedores existentes..."
docker-compose down

# Construir y ejecutar
echo "🔨 Construyendo y ejecutando contenedores..."
docker-compose up --build -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado
echo "📊 Estado de los servicios:"
docker-compose ps

# Mostrar logs
echo "📋 Logs recientes:"
docker-compose logs --tail=20

echo ""
echo "🎉 ¡MediaFind está ejecutándose!"
echo "📍 Accede a: http://localhost:8000"
echo "👤 Usuario admin: admin"
echo "🔑 Contraseña: admin123"
echo ""
echo "📝 Comandos útiles:"
echo "   Ver logs: docker-compose logs -f"
echo "   Parar: docker-compose down"
echo "   Reiniciar: docker-compose restart"
