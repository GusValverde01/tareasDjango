# 🚀 MediaFind - Guía de Inicio Rápido

## 📋 Estado Actual del Proyecto

✅ **Dockerización completada** - Archivos Docker creados
✅ **APIs integradas** - TVMaze, Jikan, Open Library, Google Books
✅ **Base de datos configurada** - Migraciones aplicadas
✅ **Sistema funcional** - Listo para usar

## 🔧 Problemas de Conectividad Detectados

- ❌ Problema de DNS/conectividad con Docker Hub
- ✅ Aplicación funciona correctamente en modo local

## 🚀 Ejecución en Modo Local (Recomendado)

### Opción 1: Script Automático
```cmd
# Ejecutar desde PowerShell en el directorio del proyecto
.\start-local.bat
```

### Opción 2: Manual
```cmd
# 1. Activar entorno virtual
venv\Scripts\activate.bat

# 2. Aplicar migraciones (si es necesario)
python manage.py migrate

# 3. Crear superusuario (si no existe)
python manage.py createsuperuser

# 4. Poblar base de datos con ejemplos
python populate_db.py

# 5. Iniciar servidor
python manage.py runserver
```

## 🌐 Acceso al Sistema

- **URL**: http://localhost:8000
- **Usuario admin**: admin
- **Contraseña**: admin123

## 🐳 Ejecución con Docker (Cuando se resuelva conectividad)

### Soluciones para problemas de Docker:

1. **Reiniciar Docker Desktop**
2. **Verificar configuración de proxy/firewall**
3. **Usar DNS alternativos (8.8.8.8, 1.1.1.1)**
4. **Configurar Docker para usar proxy corporativo si aplica**

### Comandos Docker una vez solucionado:
```bash
# Docker Compose completo
docker-compose up --build

# Docker simple (solo aplicación)
docker build -f Dockerfile.simple -t mediafind .
docker run -p 8000:8000 mediafind
```

## 🔍 Verificación de Dependencias

Ejecuta `check.bat` para verificar que todo esté instalado correctamente.

## ✨ Funcionalidades Disponibles

### 🔍 **Búsqueda Local y Externa**
- Buscar en catálogo local
- Buscar en APIs externas (TVMaze, Jikan, Open Library, Google Books)
- Importar contenido desde APIs

### 📱 **Gestión de Usuarios**
- Registro y login
- Perfiles personalizables
- Géneros y tipos de contenido favoritos

### ⭐ **Recomendaciones**
- Basadas en géneros favoritos
- Contenido popular y reciente
- Sistema de calificaciones

### 💾 **Base de Datos**
- SQLite para desarrollo local
- PostgreSQL para producción con Docker
- Datos de ejemplo incluidos

## 📂 Archivos Importantes

- `manage.py` - Comando Django principal
- `start-local.bat` - Script de inicio local
- `deploy.bat` - Script de despliegue inteligente
- `docker-compose.yml` - Configuración Docker completa
- `Dockerfile` - Imagen Docker de producción
- `requirements.txt` - Dependencias Python

## 🛠️ Comandos Útiles

```cmd
# Ver logs de desarrollo
python manage.py runserver --verbosity=2

# Acceder al shell Django
python manage.py shell

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic
```

## 🔄 Próximos Pasos

1. **Resolver conectividad Docker** para despliegue en contenedores
2. **Agregar más APIs** (películas, videojuegos) con claves gratuitas
3. **Implementar cache** con Redis
4. **Optimizar búsquedas** y rendimiento
5. **Agregar tests** automatizados

## 🆘 Troubleshooting

### Error: "Port already in use"
```cmd
# Matar proceso en puerto 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Error: "Module not found"
```cmd
# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Database locked"
```cmd
# Detener servidor y reiniciar
# Si persiste, eliminar db.sqlite3 y ejecutar migraciones
```

---

**¡MediaFind está listo para usar!** 🎉

Por favor, ejecuta `.\start-local.bat` o los comandos manuales para iniciar la aplicación.
