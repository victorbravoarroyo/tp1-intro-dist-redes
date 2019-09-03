# 75.43 Introducción a Sistemas Distribuidos
## TP #1
Este repositorio contiene el template ya usado para el ejercicio #2. Nos basaremos en él para poder implementar el TP #1.

## Inicialización
Primero, asegurarse de tener python 3 instalado: https://docs.python-guide.org/starting/install3/linux/

A continuación debemos correr los siguientes comandos, para generar el entorno y descargar las dependencias que usaremos:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Iniciar el servidor
Una vez que se ejecutan los comandos arriba mencionados, podemos proceder a inicializar el servidor. Para esto, corremos el siguiente comando:

    python app.py

## Documentación de la API y primer request

Una vez iniciado el servidor, podemos navegar a la documentación de la API. Para esto, navegamos en el browser a http://localhost:8080/api/ui.
Allí podremos encontrar todos los endpoints expuestos por la API.
Para realizar el primer request, podemos navegar en el browser a http://localhost:8080/api/alumnos.

## Resolver de DNS
Las queries de DNS que requieran contactar un servidor externo deberán ser resueltas usando 
[dnspython](http://www.dnspython.org/docs/1.16.0/). Puede verse un ejemplo
de uso en [ejemplo_resolver.py](./ejemplo_resolver.py)