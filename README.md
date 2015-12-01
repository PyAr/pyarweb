¿Queres colaborar en el proyecto? Al momento tenemos [![Stories in Ready](https://badge.waffle.io/pyar/pyarweb.png?label=ready&title=Ready)](https://waffle.io/pyar/pyarweb) tareas en
las que podes colaborar, sube a bordo! 

[![Build Status](https://travis-ci.org/PyAr/pyarweb.png)](https://secure.travis-ci.org/PyAr/pyarweb.svg?branch=master)

pyarweb
=======
Es la implementación del sitio para PyAr / Python Argentina hecha con Django
por su comunidad, wooohooo!

Mas de 20 personas sprinteando en PyconAr!!!


## ¿Cómo arranco / instalo el proyecto en mi máquina?


## Provisionamiento:

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
    $ sudo apt-get install python3-dev libxml2-dev libxslt1-dev zlib1g-dev
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

  2. Correr Celery (usando el comando dentro de tu virtualenv)

    ```
    $ python manage.py celery -A pyarweb worker --beat --autoreload --loglevel=INFO
    ```

3. Correr el servidor de desarrollo:

    En Vagrant:

    ```
    $ python3 manage.py runserver 0.0.0.0:8000
    ```

    En local:

    ```
    $ python3 manage.py runserver
    ```

  Visita con tu browser la dirección [`http://localhost:8000`](http://localhost:8000) para ver el sitio.


Para más información, si queres contribuír con el proyecto, no dejes de visitar el [*Manual básico de supervivencia para colaborar con el sitio de PyAr*](https://github.com/samuelbustamante/pyarweb/wiki/Manual-b%C3%A1sico-de-supervivencia-para-colaborar-con-el-sitio-de-PyAr).

## Cómo obtener los datos de la wiki

Además de la wiki en sí, algunas paginas especiales son gestionadas con [waliki](https://github.com/mgaitan/waliki), por lo que podrías querer los datos.

Para eso, podés clonar el repo https://github.com/PyAr/wiki.git en el directorio
`waliki_data` del root de tu proyecto (o el que indique la constante `WALIKI_DATA_DIR` de tu `local_settings.py`)

Luego de clonar el repo, tenés que sincronizar la base de datos ejecutando:

```
python manage.py sync_waliki
```

## Cargar feeds del planeta

El archivo [`fixtures/planeta_pyar.json`](fixtures/planeta_pyar.json) contiene los feeds del planeta actual, asociados al usuario con id 1.

Para cargarlos, ejecuta:

```
$ python manage.py loaddata fixtures/planeta_pyar.json
```

Más adelante habrá que asociar cada blog al usuario correspondiente.

## Contribuyendo con PyArWeb

Existen varias maneras de contribuir con la web de PyAr, reportando bugs,
revisando que esos bugs se encuentren vigentes, etc, los pasos que se
encuentran a continuación describen como realizar contribuciones a nivel de la
aplicación.

Todas las contribuciones son mas que bienvenidas, pero para empezar a
contribuir (con código) estos serían los siguientes pasos:

1. Lee el archivo [`CONTRIBUTING.md`](CONTRIBUTING.md) para entender cómo
funciona git, git-flow y tener una calidad mínima del código

2. Recuerda hacer tests! (en lo posible) de los cambios que hagas, si bien la
base de tests en este momento no es muy grande es algo que estaremos intentando
cambiar

3. Una vez tengas todo revisado haz un pull request a este proyecto
https://github.com/PyAr/pyarweb/ y haz referencia al issue.

Una vez tu pull request sea aprobado tu código pasará a la inmortalidad de
PyAr :)
