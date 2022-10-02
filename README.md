# Sistema de Gestión de Ferretería **FERME**

Repositorio para almacenar código de portafolio de titulo
Para una correcta instalación del proyecto, favor seguir las siguientes intrucciones.

El proyecto fue creado y solicita el uso de Python Version 3 y Django Version 3 o superior

## Clonamos el proyecto.
```
$ git clone https://github.com/JeanGeros/Portafolio-Ingenieria.git
```

## Instalación del entorno virtual 

* ### Instalación
    * #### Para Mac/linux:
        ```
        $ sudo pip install virtualenvwrapper
        ```
    * #### Para windows:
        ```
        $ pip install virtualenvwrapper
        ```

* ### Creación del entorno virtual       
    * #### Para mac/linux:
        ```
        $ virtualenv nameEnv
        ```
    * #### Para windows:
        ```
        $ python3 -m venv ~Nombre del enterno~
        ```
* ### Activar el entorno virtual  creado
    * #### Para mac/linux:
        ```
        $ source /~Nombre del enterno~/bin/activate/
        ```
    * #### Para windows:
        ```
        $ cd /~Nombre del enterno~/Scripts/activate/
        ```
        * #### Si no funciona intenta Esto windows:
            ```
            $ cd /~Nombre del enterno~/Scripts/
            $ cd /activate
            ```
 
## Instalar los requerimientos del proyecto
* #### Para mac/linux:
    ```
    $ sudo pip install -r requirements.txt
    ```
* #### Para windows:
    * *Intenta Esto*
        ```
        $ pip install -r requirements.txt
        ```
    * *si no, intenta instalar los requerimientos de manera manual*
        ```
        $ pip install -r requirements.txt
        $ pip freeze > requirements.txt
        ```
# Configuración Cloud
* ### Para conectar servidor cloud seguir los siguientes pasos:
 * [Configuracion Oracle Cloud](https://blogs.oracle.com/opal/post/connecting-to-oracle-cloud-autonomous-database-with-django)
  
## Crear migración del modelo de la base de datos y Aplicar modelo

```
$ python manage.py makemigrations
$ python manage.py migrate
```

## Correr Proyecto
```
$ python manage.py runserver
```

## Personaliza tu configuración 

* See 
    * [Start with Django](https://www.djangoproject.com/start/).
    * [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html)
