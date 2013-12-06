========
Usage
========

``django-periodicals`` integrates a couple other applications to provide it's features.


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

Database Setup
++++++++++++++

.. code-block :: bash

     $ python manage.py syncdb


Override Templates
==================

``django-periodicals`` provides a ``base.html`` that you may want to override to include the templates in to your existing "glue" application:

.. code-block :: bash

   $ mkdir -p myapp/templates/periodicals/

   $ emacs base.html

``django-periodicals`` defines ``title``, ``breadcrumbs``, ``innercontent`` and ``copyright`` template blocks that you can incorporate into your own base.html ``title`` and ``content`` template blocks. You might override it as follows to use your application's base template and to discard the ``breadcrumbs`` block:

.. code-block :: html

   {% extends myapp/base.html %}

   {% block breadcrumbs %}{% endblock breadcrumbs %}

   {% block content %}
   {% block innercontent %}{% endblock innercontent %}
   {% block copyright %}{% endblock copyright %}
   {% endblock content %}


Entering Data
=============

Use the Django admin pages for the Periodical application to enter data. It is easiest to proceed in this order:

#. Create a Periodical.

#. Create an Issue and select the created Periodical.

#. Create Articles and select the created Issue. Authors can be created at the same time or create one or more Author's beforehand.

Update Search Index
===================

Since adding Articles will likely be an occasional operation ``django-periodicals`` expects the Haystack index to be updated manually. Once you've finished entering all the Articles for an Issue execute this command in your virtualenv when your site is lightly loaded:

.. code-block :: bash

  $ python manage.py update_index

