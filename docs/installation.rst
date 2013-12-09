============
Installation
============

You can install from `PyPi <https://pypi.python.org/pypi>`_ and manually add some packages or install from a GitHub checkout and use ``pip`` and a ``requirement.txt`` file.


Installing from PyPi
====================

Simple to install from a package using ``pip`` which will install most of it's dependencies:

.. code-block :: bash

  $ pip install django-periodicals

Install two packages/applications manually to get newer versions than are currently in PyPi:

.. code-block :: bash

  $ pip install -e git://github.com/saschwarz/django-recaptcha.git#egg=django-recaptcha

  $ pip install -e git://github.com/nemith/django-tagging.git@dev-django1.5#egg=django_tagging-dev

Continue installing with Haystack below.


.. _installing-from-github:

Installing from GitHub
======================

This lets you install all the requirements using ``pip`` and the ``requirements.txt`` file:

.. code-block :: bash

  $ git clone https://github.com/saschwarz/django-periodicals.git

  $ cd django-periodicals

  $ pip install -r requirements.txt

  $ python setup.py install


Install a Haystack Backend
==========================

Install a search backend for use by `Haystack <http://haystacksearch.org/>`_. To start install Whoosh:

.. code-block :: bash

  $ pip install Whoosh
