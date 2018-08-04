# Contribuyendo con la web de PyAr

Podes contribuir de muchas maneras:

    Escribiendo código
    Mejorando la documentación.
    Reportando errores.


## Código de conducta

Al contribuir en este proyecto estás formando parte de la comunidad de Python Argentina. Como miembro te pedimos que
nos ayudes a mantener nuestra comunidad abierta e inclusiva. También te pedimos que leas y respetes nuestro
[*Código de Conducta*](https://ac.python.org.ar/#coc)


## Reportando errores

Una de las maneras más simples de ayudar es reportar errores. :-)

Los errores se reportan en: https://github.com/PyAr/pyarweb/issues/

* Describí siempre qué esperabas que pasé y qué sucedió en su lugar.
* De ser posible incluí un ejemplo mínimo de cómo reproducir el error.
* Incluí tracebacks, screenshots, logs de errores.
* Detallá la versiónes de tu browser, sistema operativo, etc.
* En caso que estes desarrollando con la web la versión de python que estabas utilizando.

## Escribiendo código

Configurá tu entorno
--------------------

> DISCLAIMER: si ya tenés tu fork del proyecto, esta sección no hace falta. Solo asegurate de tener el branch `master` actualizado con el _oficial_.

- Asegurate de tener instalada la [última versión de git](https://git-scm.com/downloads).
- Configurá git con tu [usuario](https://help.github.com/articles/setting-your-username-in-git/) y [email](https://help.github.com/articles/setting-your-email-in-git/)::

        git config --global user.name 'tu nombre'
        git config --global user.email 'tu email'

- Asegurate de tener una cuenta de [GitHub](https://github.com/join).
- "Forkea" *pyarweb* a tu cuenta de GitHub haciendo click en el botón de [Fork](https://github.com/PyAr/pyarweb/fork).
- [Clona](https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork) tu fork en tu computadora::

        git clone https://github.com/{username}/pyarweb
        cd pyarweb

- Agregá el repositorio principal como **remote** para posteriores actualizaciones::

        git remote add pyar https://github.com/PyAr/pyarweb
        git fetch pyar


- Ejecta pyarweb

Podés ejecutar pyarweb utilizando Docker o en tu maquina local.

[Docker](https://github.com/PyAr/pyarweb/wiki/Instalacion-con-Docker)
[Virtualenv](https://github.com/PyAr/pyarweb/wiki/Instalaci%C3%B3n-manual)


Empeza a escribir código
------------------------

> DISCLAIMER: si ya tenías tu fork del proyecto asegurate de tener el branch `master` actualizado con el _oficial_.

- Generá un nuevo branch que identifique el issue en el que vas a trabajar. (EJ: ``issue_24_nueva_funcionalidad``)
- Escribí el código utilizando tu editor preferido.

- El código debe ser [PEP8](https://pep8.org/) válido. Aunque podes ignorar el ancho de lineas. Estamos usando 99 columnas.
- Los nombres de variables y comentarios docstring son en inglés.
- Los docstrings tienen que ser de la forma """This is a docstring.""" osea,
comenzar con mayúscula y terminar con un '.' al final. Casos como: """ this is
a docstring.""" o """this is a docstring.""" o """This is a docstring""" no son
válidos.
- La identación debe ser a 4 espacios, no usar tabulador o algún tipo de
identación diferente a 4 espacios.
- Las urls deben estar escritas en español por un tema de SEO issues #163
- Todo cambio en los modelos debe ir acompañado de su respectiva migración.
- Agregar tests de los cambios suman!, sobretodo ahora que no hay suficientes ;).
- Hace push de tus commits a GitHub y [generá un a pull request](https://help.github.com/articles/creating-a-pull-request/).
- Festeja!! 🎉

Para más información consultá en el [*Manual básico de supervivencia para colaborar
con el sitio de PyAr*](https://github.com/PyAr/pyarweb/wiki/Manual-b%C3%A1sico-de-supervivencia-para-colaborar-con-el-sitio-de-PyAr).
