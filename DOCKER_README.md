# 🐳 MediaFind - Dockerized

Sistema de Búsqueda y Recomendación Multimodal dockerizado para facilitar el despliegue.

## 🚀 Inicio Rápido con Docker

### Opción 1: Docker Compose (Recomendado)

```bash
# Clonar el repositorio (si no lo tienes)
git clone <tu-repositorio>
cd tareasDjango

# Construir y ejecutar con Docker Compose
docker-compose up --build

# En segundo plano
docker-compose up -d --build
```

### Opción 2: Docker solo

```bash
# Construir la imagen
docker build -t mediafind .

# Ejecutar el contenedor
docker run -p 8000:8000 \
  -e DEBUG=True \
  -e DJANGO_SUPERUSER_USERNAME=admin \
  -e DJANGO_SUPERUSER_EMAIL=admin@mediafind.com \
  -e DJANGO_SUPERUSER_PASSWORD=admin123 \
  mediafind
```

## 🌐 Acceso

Una vez que los contenedores estén ejecutándose:

- **Aplicación**: http://localhost:8000
- **Usuario admin**: `admin`
- **Contraseña**: `admin123`
- **Base de datos PostgreSQL**: puerto 5432
- **Redis**: puerto 6379

## 📋 Servicios Incluidos

- **web**: Aplicación Django MediaFind
- **db**: Base de datos PostgreSQL 15
- **redis**: Cache y sesiones (preparado para futuras funcionalidades)

## 🔧 Variables de Entorno

### Aplicación Web
```env
DEBUG=True                              # Modo debug
SECRET_KEY=tu-clave-secreta            # Clave secreta de Django
ALLOWED_HOSTS=localhost,127.0.0.1      # Hosts permitidos
DJANGO_SUPERUSER_USERNAME=admin        # Usuario administrador
DJANGO_SUPERUSER_EMAIL=admin@email.com # Email del admin
DJANGO_SUPERUSER_PASSWORD=admin123     # Contraseña del admin
POPULATE_DB=true                       # Poblar con datos de ejemplo
```

### Base de Datos
```env
POSTGRES_DB=mediafind         # Nombre de la base de datos
POSTGRES_USER=mediafind       # Usuario de PostgreSQL
POSTGRES_PASSWORD=mediafind123 # Contraseña de PostgreSQL
```

## 📁 Volúmenes

- `./media:/app/media` - Archivos de media subidos
- `./staticfiles:/app/staticfiles` - Archivos estáticos
- `postgres_data` - Datos de PostgreSQL (persistente)

## 🛠️ Comandos Útiles

### Gestión de contenedores
```bash
# Ver logs
docker-compose logs -f web

# Acceder al contenedor
docker-compose exec web bash

# Parar servicios
docker-compose down

# Parar y eliminar volúmenes
docker-compose down -v
```

### Comandos Django en contenedor
```bash
# Migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Colectar archivos estáticos
docker-compose exec web python manage.py collectstatic

# Shell de Django
docker-compose exec web python manage.py shell

# Poblar base de datos
docker-compose exec web python populate_db.py
```

## 🔄 Desarrollo

Para desarrollo, puedes montar el código como volumen:

```yaml
# Agregar a docker-compose.yml en el servicio web:
volumes:
  - .:/app
  - ./media:/app/media
  - ./staticfiles:/app/staticfiles
```

## 🚀 Producción

Para producción, modifica las variables de entorno:

```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-super-segura
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

## 🗃️ Backup de Base de Datos

```bash
# Crear backup
docker-compose exec db pg_dump -U mediafind mediafind > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U mediafind mediafind < backup.sql
```

## 🔍 Características Dockerizadas

✅ **Auto-setup**: Se configura automáticamente al iniciar
✅ **Datos de ejemplo**: Se puebla automáticamente con contenido
✅ **APIs integradas**: TVMaze, Jikan, Open Library, Google Books
✅ **Archivos estáticos**: Servidos con WhiteNoise
✅ **Base de datos**: PostgreSQL persistente
✅ **Escalable**: Listo para múltiples instancias

## 🆘 Troubleshooting

### Error de permisos
```bash
# En Linux/Mac, asegurar permisos del script
chmod +x docker-entrypoint.sh
```

### Base de datos no conecta
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps

# Ver logs de la base de datos
docker-compose logs db
```

### Puerto ocupado
```bash
# Cambiar puertos en docker-compose.yml
ports:
  - "8001:8000"  # Cambiar 8000 por otro puerto
```

## 📦 Estructura del Proyecto

```
tareasDjango/
├── Dockerfile              # Imagen de la aplicación
├── docker-compose.yml      # Orquestación de servicios
├── docker-entrypoint.sh    # Script de inicio
├── requirements.txt        # Dependencias Python
├── .dockerignore           # Archivos excluidos
├── manage.py               # Django management
├── tareasDj4ngo/          # Configuración Django
├── tasks/                  # Aplicación principal
├── staticfiles/           # Archivos estáticos (generados)
├── media/                 # Archivos de media
└── populate_db.py         # Script de datos de ejemplo
```

¡MediaFind está listo para ejecutarse en cualquier entorno con Docker! 🎉
