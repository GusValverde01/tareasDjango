@echo off
echo 🔄 Reiniciando MediaFind con configuración mejorada...

REM Parar todos los contenedores
echo 🛑 Parando contenedores existentes...
docker-compose down
docker-compose -f docker-compose.local.yml down

REM Limpiar contenedores y redes huérfanas
echo 🧹 Limpiando recursos Docker...
docker system prune -f

REM Intentar con Docker SQLite primero (más confiable)
echo 🐳 Iniciando con SQLite (configuración simplificada)...
docker-compose -f docker-compose.local.yml up --build -d

echo ⏳ Esperando 10 segundos...
timeout /t 10 /nobreak > nul

echo 📊 Estado de los contenedores:
docker-compose -f docker-compose.local.yml ps

echo 📍 Accediendo a: http://localhost:8000
start http://localhost:8000

echo.
echo 🎉 ¡MediaFind iniciado con SQLite!
echo 👤 Usuario: admin
echo 🔑 Contraseña: admin123
echo.
echo 📝 Si hay problemas, ejecuta: .\start-local.bat
pause
