
# Sistema de Búsqueda y Recomendación Multimodal

Sistema de recomendación que permite buscar, calificar y gestionar contenido multimedia (películas, series, anime, libros, videojuegos) con integración de APIs externas.

## ✨ Características

- 🔍 **Búsqueda multimodal**: Películas, series, anime, libros y videojuegos
- 🌐 **APIs integradas**: TVMaze, Jikan (MyAnimeList), Open Library, Google Books
- 📥 **Importación automática**: Importa contenido desde APIs externas
- ⭐ **Sistema de calificaciones**: Califica y revisa contenido
- ❤️ **Favoritos personales**: Gestiona tu lista de favoritos
- 🎯 **Recomendaciones**: Basadas en géneros y preferencias

## 🚀 Instalación y Ejecución

### 🖥️ Ejecución Local

#### 1. Configuración Inicial

```bash
# Clonar el repositorio
git clone 
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

#### Opción 1: Docker Compose

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Parar servicios
docker-compose down
```

**Acceder a**: http://localhost:8000

### Credenciales por Defecto

- **Usuario**: admin
- **Contraseña**: admin123


