
## Instalar proyecto y ejecución 

Instalar pip install virtualenv

Activar virtualenv venv

Usar Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

Activar el entorno virtual con .\venv\Scripts\activate

pip install django 

django-admin startproject tareasDj4ngo . 

python manage.py runserver 

Abrir el servidor http://127.0.0.1:8000/


## Crear carpeta 

Con el entorno activado: 
python manage.py startapp tasks 