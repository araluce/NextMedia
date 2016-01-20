# NextMedia

[![Build Status](https://travis-ci.org/araluce/NextMedia.svg?branch=master)](https://travis-ci.org/araluce/NextMedia)

## HITO 1

Este nuevo proyecto, consta de la realizacion de una infraestructura virtual para un proyecto de subida,carga y vision de videos a traves de una aplicacion web.
Mi parte a desarrollar en este proyecto, consta de la gestión de videos de la base de datos:

* Subir vídeo.

* Modificar vídeo.

* Eliminar vídeo.

* Parte de la web referente al vídeo.


Y la parte conjunta en colaboración de mi compañero constará de la unificación de la base de datos de usuarios con la gestión de vídeos de la página y funcionamiento con su aplicación web.

Este proyecto dará soporte a una aplicación web que implementaré para la asignatura DAI.

Cada usuario, podrá subir el vídeo que desee y poder reproducirlo en la aplicación.

## HITO 2

En esta parte del proyecto desarrollada en **python** hemos realizado la integración continua del proyecto **NextMedia**.
Hemos utilizado las herramientas:

* **Django** (marco MVC)
* **wheel**
* **pycco** (documenta el código python)
* **Travis-CI** (integración continua)

Los **test** en lenguaje de programación python, se ejecutan en django que esta basado en unittest.

Para la integración continua he utilizado **Travis-CI**.

El código del fichero **.travis.yml** es el siguiente:

```
language: python
python:
 - "2.7"
# command to install dependencies
install:
 - sudo apt-get install python-dev
 - pip install -q Django==1.8.5
 - pip install -q wheel==0.24.0
 - pip install pycco
# command to run tests
script:
 - pycco NextMedia/*.py
 - pycco NextMedia/app/*.py
 - python NextMedia/manage.py test NextMedia

branches:
  - only:
    - master

```

También he creado un makefile para automatizar el proceso de instalación, testeo, documentación y ejecución del server:

```
install:
    sudo python NextMedia/setup.py install

test:
    python NextMedia/manage.py test

doc:
    pycco NextMedia/*.py
    pycco NextMedia/app/*.py

run:
    python NextMedia/manage.py runserver
```

Y el resultado de su ejecución es el siguiente:
![Resultado de travis.yml](http://imageshack.com/a/img907/3985/PML0Kq.png)
## PROYECTO EN COLABORACIÓN:

[Álvaro Fernández-Alonso Araluce](https://github.com/araluce/NextMedia)

[Alejandro Reyes Portellano](https://github.com/reyic/NextMedia)
