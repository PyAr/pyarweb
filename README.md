¿Queres colaborar en el proyecto? Al momento tenemos [![Stories in Ready](https://badge.waffle.io/pyar/pyarweb.png?label=ready&title=Ready)](https://waffle.io/pyar/pyarweb) tareas en
las que podes colaborar, sube a bordo! 
pyarweb
=======
Es la implementación del sitio para PyAr / Python Argentina hecha con Django
por su comunidad, wooohooo!

Mas de 20 personas sprinteando en PyconAr!!!


## Como trabajar con Github y los pull requests?

1- Tener una cuenta en github, y estar logueado en github.

2- Ingresar a https://github.com/PyAr/pyarweb, y forkear el proyecto.
Al forkear el proyecto, github hace una copia entera del proyecto y lo
crea como un repositorio donde vos sos el propietario, osea un repositorio
tuyo. Es como un "copy/paste" desde la "compu de pyar" a tu "compu". Esto
quiere decir que las modificaciones que hagas en el fuente estarán en tu
repositorio, pero no en el repositorio de PyAr. Para poder enviar las
modificaciones presentes en tu repositorio (en tu fork), es que luego vas
a crear un Pull Request. Podes forkear el proyecto de PyAr haciendo click
en el botón "Fork" que lo podes encontrar en la parte superior a la derecha.

3- Una vez forkeado el proyecto, te lo clonas. Siempre recordar trabajar
sobre el branch "develop". A continuación un ejemplo: 

::

    [edvm@laptop mixes] $ git clone git@github.com:edvm/pyarweb.git pyar
    Cloning into 'pyar'...
    remote: Counting objects: 3007, done.
    remote: Total 3007 (delta 0), reused 0 (delta 0), pack-reused 3006
    Receiving objects: 100% (3007/3007), 822.01 KiB | 73.00 KiB/s, done.
    Resolving deltas: 100% (1917/1917), done.
    Checking connectivity... done.
    [edvm@laptop mixes] $ cd pyar
    [edvm@laptop pyar] (master) $ git checkout develop
    Branch develop set up to track remote branch develop from origin.
    Switched to a new branch 'develop'
    [edvm@laptop pyar] (develop) $ git branch -r
      origin/HEAD -> origin/master
      origin/develop
      origin/master
      origin/waliki
    [edvm@laptop pyar] (develop) $ git pull origin develop
    From github.com:edvm/pyarweb
     * branch            develop    -> FETCH_HEAD
    Already up-to-date.
    [edvm@laptop pyar] (develop)


4- Ahora metes código. Te tiro un tip por si no lo conocías, usar "git flow"
es genial! http://nvie.com/posts/a-successful-git-branching-model/

5- Perfecto, hiciste tus modificaciones, y las pusheaste al branch "develop",
por ejemplo:

:: 
    [edvm@laptop pyar] (develop) $ git push origin develop
    Counting objects: 3, done.
    Delta compression using up to 2 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 1.51 KiB | 0 bytes/s, done.
    Total 3 (delta 2), reused 0 (delta 0)
    To git@github.com:edvm/pyarweb.git
       1925eca..9c2f38c  develop -> develop
    [edvm@laptop pyar] (develop)

6- Genial, ahora tus cambios están subidos a tu branch "develop" en Github.
Queres integrar esos cambios con el branch "develop" de PyAr, y la forma
en que se hace es creando a lo que le llaman "Pull Request", que le
pusieron ese nombre, pero para mi tiene más sentido si se llamara 
"Push Request", porque lo que queres hacer es mandar/"pushear" código jeje.
Bueno, para crear el Pull Request vas a la url de tu fork, en mi caso es:
https://github.com/edvm/pyarweb/tree/develop

Asegurate de seleccionar como branch "develop", vas a ver un botón verde
que dice "Compare and Pull Request". Le das click, te va a pedir algunos
datos. El title sería como el "subject", un mensaje corto bien descriptivo
por ejemplo: "Resuelvo el issue #13", y en el body/cuerpo del mensaje, si
lo consideras necesario podes escribir lo que quieras. Finalmente le das
click al botón verde "Create pull request", eso es todo! Lo que acaba de
suceder, es que el repositorio "PyAr" recibe una notificación de que hay
un "Pull Request" pendiente de revisión. En ese momento se revisa el
PR (pull request) y si todo esta ok, PyAr acepta el PR y tus cambios 
quedan integrados en el repositorio de PyAr. Puede también suceder que
no se acepte el PR y te comenten el porque no se aceptó, quizá hay algún
error en el código, etc. Animos! es cuestión de corregir lo comentado,
y volver a comenzar desde el punto 4 :).  

7- Más referencias sobre los pull requests:

- https://help.github.com/articles/creating-a-pull-request/
   

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
python manage.py sync_waliki
```

## Cargar feeds del planeta

El archivo [`fixtures/planeta_pyar.json`](fixtures/planeta_pyar.json) contiene los feeds del planeta actual, asociados al usuario con id 1.

Para cargarlos, ejecuta:

```
$ python manage.py loaddata fixtures/planeta_pyar.json
```

Más adelante habrá que asociar cada blog al usuario correspondiente.
