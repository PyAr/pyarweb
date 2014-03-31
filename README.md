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

1- Debes crear un nuevo virtualenv, Ej: pyvenv3-3 pyarweb 

Activas tu virtualenv, ej: source pyarweb/bin/activate

Si no pip instalado, descarga el .tar.gz desde https://pypi.python.org/pypi/setuptools
e instalalo con el python3 de tu virtualenv. Luego de instalar setuptools hacer:

easy_install-3.3 pip

2. Instalar django-disqus a mano: 

git clone https://github.com/PyAr/django-disqus.git

cd django-disqus; python ./setup.py develop

2. instalar las dependencias, ej: pip3 install -r ./requirements.txt

3. python manage.py syncdb

4. python manage.py runserver

5. Visitar con tu browser http://localhost:8000  y listo!

Para más información, si queres contribuír con el proyecto, no dejes de visitar:

https://github.com/samuelbustamante/pyarweb/wiki/Manual-b%C3%A1sico-de-supervivencia-para-colaborar-con-el-sitio-de-PyAr
