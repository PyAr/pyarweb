# Contribuyendo con la web de PyAr

## Calidad mínima del código

1. El código debe ser pep8 válido.
2. Los nombres de variables y comentarios docstring son en inglés.
3. Los docstrings tienen que ser de la forma """This is a docstring.""" osea,
comenzar con mayúscula y terminar con un '.' al final. Casos como: """ this is
a docstring.""" o """this is a docstring.""" o """This is a docstring""" no son
válidos.
4. La identación debe ser a 4 espacios, no usar tabulador o algún tipo de
identación diferente a 4 espacios.
5. Las urls deben estar escritas en español por un tema de SEO issues #163
6. Todo cambio en los modelos debe ir acompañado de su respectiva migración.
7. Agregar tests de los cambios suman!, sobretodo ahora que no hay suficientes
   ;).

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


4- Hacer tus modificaciones en el branch "develop" no es la mejor práctica. 
Un pull-request en github representa una peticion de merge (de pull = fetch + merge), 
y como tal, todos los commits que estén en la rama "que se pide mezclar" 
irán a parar a la rama destino. Esto significa, siguiendo las buenas practicas 
de git-flow que se menciona más abajo, que lo mejor es hacer un branch local, 
hacer todos los commits allí, pushear ese branch al repo propio y crear el PR 
contra el develop de pyar. Los PR develop -> develop complican trabajar en dos 
o más pull request en paralelo y sincronizar con el branch upstream (el "develop" oficial) 
Te tiro un tip por si no lo conocías, usar "git flow" es genial! 
http://nvie.com/posts/a-successful-git-branching-model/

5- Perfecto, entonces instalate "git flow", te lees el link de arriba para
entender que hace/significa git flow, una vez hecho eso comenzas a trabajar
por ejemplo en el issue-20:
 
    [edvm@laptop pyar] (develop) $ git flow feature start issue-20 
    Switched to a new branch 'feature/issue-20'
    Summary of actions:
    - A new branch 'feature/issue-20' was created, based on 'develop'
    - You are now on branch 'feature/issue-20'
    Now, start committing on your feature. When done, use:
         git flow feature finish issue-20 
    [edvm@laptop pyar] (feature/issue-20) 

Es importante leer lo que te dice la consola, quiero resaltar las siguientes
dos lineas:

    - A new branch 'feature/issue-20' was created, based on 'develop'
    - You are now on branch 'feature/issue-20'

Esto quiere decir que un nuevo branch llamado 'feature/issue-20' fue creado
a partir de 'develop', y que ahora vos estas parado sobre el branch 
'feature/issue-20'.

Ahora meto codigo, modifico, comiteo, comiteo, comiteo muy seguido, una
vez termino con mi tarea es hora de integrar los cambios que acabo de
hacer al branch "develop" de mi compu, el local, por ejemplo: 

    [edvm@laptop pyar] (feature/issue-20) $ git flow feature finish issue-20 
    Switched to branch 'develop'
    Your branch is up-to-date with 'origin/develop'.
    Already up-to-date.
    Deleted branch feature/issue-20 (was ba56278).
    Summary of actions:
    - The feature branch 'feature/issue-20' was merged into 'develop'
    - Feature branch 'feature/issue-20' has been removed
    - You are now on branch 'develop'
    [edvm@laptop pyar] (develop) $

Repasando el "summary of actions", lo que acaba de hacer:

    - The feature branch 'feature/issue-20' was merged into 'develop'
    - Feature branch 'feature/issue-20' has been removed
    - You are now on branch 'develop'

Primero hizo merge de los cambios existentes en el branch 'feature/issue-20'
al branch 'develop', luego borra el branch local 'feature/issue-20' (que es
el branch local), y te deja parado en el branch 'develop'.

Finalmente subis tus cambios a Github:

    [edvm@laptop pyar] (develop) $ git push origin develop
    ....


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
 
Para más información consultá en el [*Manual básico de supervivencia para colaborar 
con el sitio de PyAr*](https://github.com/PyAr/pyarweb/wiki/Manual-b%C3%A1sico-de-supervivencia-para-colaborar-con-el-sitio-de-PyAr).
