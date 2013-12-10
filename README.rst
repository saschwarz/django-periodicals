=============================
django-periodicals
=============================

.. image:: https://badge.fury.io/py/django-periodicals.png
    :target: http://badge.fury.io/py/django-periodicals
    
.. image:: https://travis-ci.org/saschwarz/django-periodicals.png?branch=master
        :target: https://travis-ci.org/saschwarz/django-periodicals

.. image:: https://pypip.in/d/django-periodicals/badge.png
        :target: https://crate.io/packages/django-periodicals?version=latest


A Django application for periodical/magazine websites with fully cross linked indices on Periodical, Issue, Article, Author, Article Series and Tags. Provides full text search of article titles and descriptions. A complete set of templates are provided. A sitemap is also dynamically generated.

Documentation
-------------

The full documentation is at http://django-periodicals.rtfd.org.

Quickstart
----------

Simple to install from a package using ``pip`` which will install all it's dependencies (coming soon). For now see `installing-from-github <http://django-periodicals.readthedocs.org/en/latest/installation.html#installing-from-github>`_.

.. code-block :: bash

    pip install django-periodicals

Install two packages manually to get newer versions than are currently in `PyPi <https://pypi.python.org/pypi>`_:

.. code-block :: bash

  $ pip install -e git://github.com/saschwarz/django-recaptcha.git#egg=django-recaptcha

  $ pip install -e git://github.com/nemith/django-tagging.git@dev-django1.5#egg=django_tagging-dev


Install a search backend for use by `Haystack <http://haystacksearch.org/>`_. To start install Whoosh:

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

Configure your Haystack backend. Here is an example using `Whoosh <https://bitbucket.org/mchaput/whoosh/wiki/Home>`_:

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

Configure your reCAPTCHA keys - only used when users add links to Articles or Issues:

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

I developed ``django-periodicals`` to provide a searchable index for a printed magazine. I wanted all the meta data to be fully cross linked. So users can easily browse all articles for an author, all articles in an issue, all articles in a series/category, all articles tagged with a keyword and so forth. 

I turned it in to a standalone application when I ported it to Django 1.5. Here are the features:

* Provides Django models for Periodicals, Issues, Articles, Authors, Tags and Links to external material. 

* A full set of templates are provided including:

  * Individual Periodical pages with yearly indices.

  * Fully cross-linked indexes of Authors, Issues, Article Series, Tags, and Articles.

  * Search across Article titles and descriptions.

  * Tagging:

    * Per article.

    * Index pages per tag.

    * Tag cloud.

* Moderated user added links of blog posts and other web resources to each Issue and Article. Spam protection by `reCAPTCHA <http://www.google.com/recaptcha>`_ and requiring approval by the admin.

* Django admin forms for data entry.

* Sitemap support.

* Support for Python 2.6, 2.7 and Django 1.5 and 1.6.

* Travis CI unit tests.

* See ``django-periodicals`` in action at `Googility <http://googility.com/periodicals/>`_.
