Movie Planet
============

Simple API with movies, comments and ranking. MoviePlanet is using OMDb API for fetching movies.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT

Prerequisites
--------------
* Docker
* Docker Compose

Basic
--------------

Setting Up Your Project
^^^^^^^^^^^^^^^^^^^^^^^


* To run postgres database, use this command::

    $ docker-compose -f local.yml up -d postgres

* To run migrations, use this command::

    $ docker-compose -f local.yml run --rm --no-deps --service-ports django python manage.py migrate

* Generate your OMDB API KEY and add it to environment variables::

    for generate API KEY visit http://www.omdbapi.com/apikey.aspx
    add to your .env/.local/.django
    OMDB_API_KEY and OMDB_URL

* To run application, use this command::

    $ docker-compose -f local.yml run --rm --no-deps --service-ports django

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage::

    $ docker-compose -f local.yml run django coverage run -m pytest
    $ docker-compose -f local.yml run django coverage report

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ docker-compose -f local.yml run django pytest

Postman Collection
^^^^^^^^^^^^^^^^^^

::

    * postman collection can be found in `/movie_planet/postman/` directory

