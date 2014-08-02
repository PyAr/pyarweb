pyarweb
=======
Es la implementación del sitio para PyAr / Python Argentina hecha con Django
por su comunidad, wooohooo!.

Inquietud:
----------
Como arranco / instalo el proyecto en mi máquina?

Respuesta: 
----------

Debes tener python3, NO codeamos el sitio con compatibilidad con python.

1- Debes crear un nuevo virtualenv
    Ej 1 usando pyvenv: pyvenv3-3 pyarweb 
    Ej 2 usando virtualenvwrapper: export VIRTUALENV_PYTHON=/usr/bin/python3
                                   mkvirtualenv pyarweb

Activas tu virtualenv
    Ej 1: source pyarweb/bin/activate
    Ej 2 usando virtualenvwrapper: workon pyarweb 

Si no pip instalado, descarga el .tar.gz desde https://pypi.python.org/pypi/setuptools
e instalalo con el python3 de tu virtualenv. Luego de instalar setuptools hacer:

easy_install-3.3 pip

2. sudo apt-get install python3-dev (PIL se mal copa si no lo tenes instalado)

3. instalar las dependencias, ej: pip3 install -r ./requirements.txt

4. python manage.py syncdb

5. python manage.py runserver

6. Visitar con tu browser http://localhost:8000  y listo!

Para más información, si queres contribuír con el proyecto, no dejes de visitar:

https://github.com/samuelbustamante/pyarweb/wiki/Manual-b%C3%A1sico-de-supervivencia-para-colaborar-con-el-sitio-de-PyAr
