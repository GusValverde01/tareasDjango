
## Instalar proyecto y ejecución 

Clonar el repositorio: 

git clone https://github.com/GusValverde01/tareasDjango.git

Instalar el Entorno Virtual:

pip install virtualenv

Crear carpeta venev para Entorno Vitual:

virtualenv venv

Usar Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

Activar el entorno virtual:

.\venv\Scripts\activate

## Instalar Django con el entorno virtual activado (venv):

pip install django 

django-admin startproject tareasDj4ngo . 

## Iniciar el Desarrrollo

python manage.py runserver 

Abrir el servidor http://127.0.0.1:8000/


## Evidencias de Funcionamiento

Login:

![image](https://github.com/user-attachments/assets/90f67767-7840-4d7f-b0dd-318cc673b77e)

Registrar Usuario:

![image](https://github.com/user-attachments/assets/41306bf5-1eed-4e75-b29d-3f77dec46b2f)

Página Home para Usuarios:

![image](https://github.com/user-attachments/assets/8bccdf2f-0542-42c4-a8b5-96fcf3dc79f2)

## Crear carpetas

Con el entorno activado: 
python manage.py startapp NOMBRE 

