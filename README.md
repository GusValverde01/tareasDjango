
# 🎬 MediaFind - Sistema de Búsqueda y Recomendación Multimodal

Sistema de recomendación que permite buscar, calificar y gestionar contenido multimedia (películas, series, anime, libros, videojuegos) con integración de APIs externas.

## ✨ Características

- 🔍 **Búsqueda multimodal**: Películas, series, anime, libros y videojuegos
- 🌐 **APIs integradas**: TVMaze, Jikan (MyAnimeList), Open Library, Google Books
- 📥 **Importación automática**: Importa contenido desde APIs externas
- ⭐ **Sistema de calificaciones**: Califica y revisa contenido
- ❤️ **Favoritos personales**: Gestiona tu lista de favoritos
- 🎯 **Recomendaciones**: Basadas en géneros y preferencias

## 🚀 Instalación y Ejecución

### 📋 Requisitos Previos

- Python 3.8+ 
- Git
- Docker (opcional, para contenedores)

### 🖥️ Ejecución Local (Recomendado)

#### 1. Configuración Inicial

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd tareasDjango

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 2. Configurar Base de Datos

```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Poblar con datos de ejemplo (opcional)
python populate_db.py
```

#### 3. Ejecutar Servidor

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

```

**Acceder a**: http://localhost:8000

### 🐳 Ejecución con Docker

#### Opción 1: Docker Compose (Completo con PostgreSQL)

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# En segundo plano
docker-compose up -d --build

# Ver logs
docker-compose logs -f web

# Parar servicios
docker-compose down
```

#### Opción 2: Docker Simple (Solo aplicación)

```bash
# Construir imagen
docker build -t mediafind .

# Ejecutar contenedor
docker run -p 8000:8000 \
  -e DEBUG=True \
  -e DJANGO_SUPERUSER_USERNAME=admin \
  -e DJANGO_SUPERUSER_EMAIL=admin@mediafind.com \
  -e DJANGO_SUPERUSER_PASSWORD=admin123 \
  mediafind
```

#### Opción 3: Script Automático (Windows)

```cmd
# Ejecutar script inteligente que detecta el mejor método
.\deploy.bat
```

**Acceder a**: http://localhost:8000

## 📱 Uso del Sistema

### 🔐 Credenciales por Defecto

- **Usuario**: admin
- **Contraseña**: admin123

### 🌟 Funcionalidades Principales

1. **🏠 Página Principal**
   - Contenido popular y reciente
   - Recomendaciones personalizadas
   - Búsqueda rápida

2. **🔍 Búsqueda Avanzada**
   - Búsqueda local en tu catálogo
   - Búsqueda en APIs externas
   - Filtros por tipo, género, calificación
   - Importación directa desde APIs

3. **👤 Gestión de Perfil**
   - Personalizar géneros favoritos
   - Configurar tipos de contenido preferidos
   - Ver estadísticas personales

4. **⭐ Calificaciones y Favoritos**
   - Calificar contenido (1-10 estrellas)
   - Agregar reseñas personales
   - Gestionar lista de favoritos

### APIs Sin Credenciales (Funcionando)

- **📺 TVMaze API**: Series y programas de TV
- **🎌 Jikan API**: Anime y manga (MyAnimeList)
- **📚 Open Library**: Libros y autores
- **📖 Google Books**: Libros con previews y ratings

## 🛠️ Comandos de Desarrollo

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test

# Poblar base de datos
python populate_db.py
```

## 🐳 Comandos Docker

```bash
# Ver servicios activos
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Acceder al contenedor web
docker-compose exec web bash

# Ejecutar comandos Django en contenedor
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Reiniciar servicios
docker-compose restart

# Limpiar todo (incluye volúmenes)
docker-compose down -v
```

## 📊 Servicios Docker

- **web**: Aplicación Django MediaFind
- **db**: PostgreSQL 15 (base de datos)
- **redis**: Redis (cache y sesiones)

## 🔧 Variables de Entorno

```env
# Django
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos (solo Docker)
DATABASE_URL=postgresql://user:pass@db:5432/mediafind

# Usuario admin
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@mediafind.com
DJANGO_SUPERUSER_PASSWORD=admin123

# Configuración
POPULATE_DB=true
```

