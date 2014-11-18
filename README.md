pyarweb
=======
Es la implementación del sitio para PyAr / Python Argentina hecha con Django
por su comunidad, wooohooo!.

Mas de 20 personas sprinteando en PyconAr!!!


Inquietud:
----------
Como arranco / instalo el proyecto en mi máquina?

Respuesta:
----------

Debes tener python 3.3 o 3.4, no hay compatibilidad con python 2.

1- Debes crear un nuevo virtualenv

    Ej 1 usando pyvenv: pyvenv3-3 pyarweb

    Ej 2 usando virtualenvwrapper: 

        export VIRTUALENV_PYTHON=/usr/bin/python3

        mkvirtualenv pyarweb

Activas tu virtualenv

    Ej 1: source pyarweb/bin/activate

    Ej 2 usando virtualenvwrapper: workon pyarweb

Si no tenés pip instalado, descarga el .tar.gz desde https://pypi.python.org/pypi/setuptools
e instalalo con el python3 de tu virtualenv. Luego de instalar setuptools hacer:

easy_install-3.3 pip

2. sudo apt-get install python3-dev libxml2-dev libxlst1-dev

3. Instalar las dependencias, ej: pip3 install -r ./requirements.txt

4. (Para poder usar el Planeta PyAr):
    a. Instalar Redis, ej: sudo apt-get install redis-server
    b. Correr Celery (usando el comando dentro de tu virtualenv), ej: /bin/celery -A pyarweb worker -B --loglevel=INFO

5. python manage.py syncdb

6. python manage.py runserver

7. Visitar con tu browser http://localhost:8000  y listo!

Para más información, si queres contribuír con el proyecto, no dejes de visitar:

https://github.com/samuelbustamante/pyarweb/wiki/Manual-b%C3%A1sico-de-supervivencia-para-colaborar-con-el-sitio-de-PyAr

## Como obtener los datos de la Wiki

Ademas de la wiki en si, algunas paginas especiales son gestionadas con waliki, por lo que podrias querer los datos.

Para eso podes clonar el repo https://github.com/PyAr/wiki.git en el directorio
`waliki_data` del root de tu proyecto (o el que indique la constante `WALIKI_DATA_DIR` de tu `local_settings.py`)

Luego de clonar el repo, tenes que sincronizar la base de datos ejecuntando

```
python manage sync_waliki
```

