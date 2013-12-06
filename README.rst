=============================
django-periodicals
=============================

.. image:: https://badge.fury.io/py/django-periodicals.png
    :target: http://badge.fury.io/py/django-periodicals
    
.. image:: https://travis-ci.org/saschwarz/django-periodicals.png?branch=master
        :target: https://travis-ci.org/saschwarz/django-periodicals

.. image:: https://pypip.in/d/django-periodicals/badge.png
        :target: https://crate.io/packages/django-periodicals?version=latest


A Django app for periodical/magazine websites with tagging and search.

Documentation
-------------

The full documentation is at http://django-periodicals.rtfd.org.

Quickstart
----------

Simple to install from a package using ``pip`` which will install all it's dependencies:

.. code-block :: bash

    pip install django-periodicals

Install two packages manually to get newer versions than are currently in `PyPi <https://pypi.python.org/pypi>`_:

.. code-block :: bash

  $ pip install -e git://github.com/saschwarz/django-recaptcha.git#egg=django-recaptcha

  $ pip install -e git://github.com/nemith/django-tagging.git@dev-django1.5#egg=django_tagging-dev

Install a search backend for use by `Haystack <http://haystacksearch.org/>`_. To play around just install Whoosh:

.. code-block :: bash

  $ pip install Whoosh

settings.py
+++++++++++

Add ``periodicals`` and the other applications it uses to ``INSTALLED_APPS``:

.. code-block :: python

    INSTALLED_APPS = (
        ...
        'haystack',
        'tagging',
        'captcha',
        'periodicals',
    )

Configure your Haystack backend:

.. code-block :: python

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'whoosh_periodicals_index'),
            'STORAGE': 'file',
            'POST_LIMIT': 128 * 1024 * 1024,
            'INCLUDE_SPELLING': True,
            'BATCH_SIZE': 100,
        },
    }

Configure your reCAPTCHA keys:

.. code-block :: python

    RECAPTCHA_PRIVATE_KEY = "your-recaptcha-private-key"
    RECAPTCHA_PUBLIC_KEY = "your-recaptcha-public-key"


urls.py
+++++++

Choose a URL prefix at which to base the application:

.. code-block :: python

    ...
    import periodicals

    urlpatterns = patterns('',
        ...
        url(r'^admin/', include(admin.site.urls)),
        url(r'^periodicals/', include(periodicals.urls)),
    )

Management Commands
+++++++++++++++++++

.. code-block :: bash

    $ python manage.py syncdb
  

Features
--------

* Provides Django models for Periodicals, Issues, Articles and Authors.

* A full set of templates are provided including:

  * Individual Periodical pages with yearly indices

  * Index of Authors, Issues, Article Series

  * Search across Article titles and descriptions

  * Tagging:

    * Per article

    * Index pages per tag

    * Tag cloud

* Users added links of blog posts and other web resources to each Issue and Article. Protected by `reCAPTCHA <http://www.google.com/recaptcha>`_ and requiring approval by the admin.

* Use the Django admin to enter each of the data model instances.

* See ``django-periodicals`` in action at `Googility <http://googility.com/periodicals/>`_.
