[![Stories in Ready](https://badge.waffle.io/PyAr/pyarweb.png?label=ready&title=Ready)](https://waffle.io/PyAr/pyarweb)
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

2. Activas tu virtualenv.

  * Mediante *source*

      ```
      $ source pyarweb/bin/activate
      ```

  * Mediante *virtualenvwrapper*

      ```
      $ workon pyarweb
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
    $ python manage.py syncdb
    ```

2. Correr Celery para Planeta PyAr:

  2. Correr Celery (usando el comando dentro de tu virtualenv)

    ```
    $ celery -A pyarweb worker --beat --autoreload --loglevel=INFO
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
python manage sync_waliki
```

## Cargar feeds del planeta

El archivo [`fixtures/planeta_pyar.json`](fixtures/planeta_pyar.json) contiene los feeds del planeta actual, asociados al usuario con id 1.

Para cargarlos, ejecuta:

```
$ python manage.py loaddata fixtures/planeta_pyar.json
```

Más adelante habrá que asociar cada blog al usuario correspondiente.
