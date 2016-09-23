[![Build Status](https://travis-ci.org/PyAr/pyarweb.png)](https://secure.travis-ci.org/PyAr/pyarweb.svg?branch=master)

pyarweb
=======

Esta es la implementación del [sitio para PyAr / Python Argentina](http://python.org.ar) hecha con Django
por su comunidad, wooohooo!

Decenas de personas han colaborado de [diversas maneras](https://github.com/PyAr/pyarweb/wiki/Contribuyendo-con-PyArWeb).
¡Gracias por eso! Y vos ¿te querés sumar?

## ¿Cómo arranco / instalo el proyecto en mi máquina?


### Via [Docker](http://docker.com) (recomendando):


1. Instalar [docker-compose](https://docs.docker.com/compose/install/) de la manera recomendada
   para tu sistema operativo. En windows podés usar


2. Hacé un fork y cloná el proyecto localmente.


2. Construir la imágen para la aplicación. Esto bajará e instalará todas las dependencias dentro
   de un contenedor, sin modificar el equipo anfitrión:

        $ cd path/to/pyarweb
        $ docker-compose build

3. Inicializá la base de datos.

      $ docker-compose run web ./initialize.sh


4. Levantá los servicios

        $ docker-compose up -d


¡Listo! Visitá la dirección [`http://localhost:8000`](http://localhost:8000) para ver el sitio.
Un usuario administrador `admin` con password `admin` ya debería estar cargado.

De ahora en más, para ejecutar comandos dentro del container debés precederlos con `docker-compose run web`.
Por ejemplo, para entrar en el shell de django, ejecutá:

      $ docker-compose run web python3 manage.py shell

También podés ejecutar `docker-compose run web bash` y directamente *pasarte* a la consola bash del
contenedor

### ¿Y sin docker?

Si no te gusta o no podés usar docker y querés instalar todo el entorno en tu propia maquina, podés ver
instrucciones generales en [esta página de la wiki](https://github.com/PyAr/pyarweb/wiki/Instalaci%C3%B3n-manual)

## Más info

Para más información visitá (y contribuí!) a nuestra [wiki de desarrollo](https://github.com/PyAr/pyarweb/wiki)


