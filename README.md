[![Build Status](https://travis-ci.org/PyAr/pyarweb.png)](https://secure.travis-ci.org/PyAr/pyarweb.svg?branch=master)

pyarweb
=======

Esta es la implementación del [sitio para PyAr / Python Argentina](http://python.org.ar) hecha con Django
por su comunidad, wooohooo!

Decenas de personas han colaborado de [diversas maneras](https://github.com/PyAr/pyarweb/wiki/Contribuyendo-con-PyArWeb).
¡Gracias por eso! Y vos ¿te querés sumar?

## ¿Cómo arranco / instalo el proyecto en mi máquina?


## Provisionamiento:


### Con Docker (Recomendado)

1. Instalar [Docker](https://docs.docker.com/engine/installation/)

2. Clona / Forkea el repositorio. Dentro del directorio *scripts* se encuentra el
archivo *webcli.py*, Ejecutalo pasando --help para ver las opciones disponibles:

    ```
    edvm@debian:~/Repos/edvm/pyarweb (develop)*$ ./scripts/webcli.py --help
    usage: webcmd [-h] [--build-image] [--run-container] [--del-container]
                  [--run-shell]

    Helper to start a Pyarweb development instance.

    optional arguments:
      -h, --help       show this help message and exit
      --build-image    Build PyAr web docker image
      --run-container  Creates the docker container 
      --del-container  Removes PyAr web container
      --run-shell      Exec a bash interpreter on a running containe

    ```

    2.1.  Crea la imagen (build) localmente, para ello ejecuta: `scripts/webcli.py --build-image`

    2.2.  Crea el container a partir de la imagen generada anteriormente, para ello ejecuta: `scripts/webcli.py --run-container`.

3. Una vez ejecutado `scripts/webcli.py --run-container`, debes:

    3.1  Instala los requirements con: `pip install -r /opt/code/requirements.txt` 

    3.2  Corre los migrations con: `cd /opt/code && ./manage.py migrate` 

4. Corre el proyecto con: `./manage.py runserver 0.0.0.0:8000`

5. Abre tu navegador apuntando a: `http://127.0.0.1:8000`


### Con Vagrant:

1. Instalar [VirtualBox](https://www.virtualbox.org/) y [Vagrant](https://www.vagrantup.com/).

2. Levantar maquina virtual (esto ya instala todas las dependencias):

        $ cd path/to/pyarweb
        $ vagrant up

3. Entrar a la maquina virtual y levantar servicios:

        $ cd path/to/pyarweb
        $ vagrant ssh
        vagrant@vagrant $ cd /vagrant/

### Sin Vagrant:


Debes tener Python 3.3 o 3.4, no hay compatibilidad con Python 2.

1. Debes crear un nuevo virtualenv.

  	* Usando *pyvenv*

      ```
	    $ pyvenv3-3 pyarweb
      ```

    * Usando *virtualenvwrapper*

      ```
      $ export VIRTUALENV_PYTHON=/usr/bin/python3
      $ mkvirtualenv pyarweb
      ```

    * Usando *virtualenv*

      ```
      $ virtualenv -p /usr/bin/python3.4 pyarweb
      ```


2. Activas tu virtualenv.

  * Mediante *source*

      ```
      $ source pyarweb/bin/activate
      ```

  * Mediante *virtualenvwrapper*

      ```
      $ workon pyarweb
      ```

  * Mediante *virtualenv*

      ```
      $ source pyarweb/bin/activate
      ```

3. Si no tenés pip instalado, descarga el .tar.gz desde https://pypi.python.org/pypi/setuptools
e instalalo con el `python3` de tu virtualenv. Luego de instalar setuptools hacer:

    ```
    $ easy_install-3.3 pip
    ```

4. Instalar librerías de desarrollo.

    ```
    $ sudo apt-get install python3-dev libxml2-dev libxslt1-dev zlib1g-dev libffi-dev
    ```

5. Instalar las dependencias.

    ```
    $ pip3 install -r ./requirements.txt
    ```

6. Instalar Redis

    ```
    $ sudo apt-get install redis-server
    ```

## Correr Servicios:

1. Sincronizar BD con los modelos:

    ```
    $ python manage.py migrate
    ```

2. Correr Celery para Planeta PyAr:

1. Instalar [docker-compose](https://docs.docker.com/compose/install/) de la manera recomendada
   para tu sistema operativo. 


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


