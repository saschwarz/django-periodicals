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

Configure your reCAPTCHA keys - only used when users add links to Articles or Issues (this feature can be disabled):

.. code-block :: python

    RECAPTCHA_PRIVATE_KEY = "your-recaptcha-private-key"
    RECAPTCHA_PUBLIC_KEY = "your-recaptcha-public-key"

Configure you Site in the Django Site application - only used when users add links to Articles or Issues *and* when you haven't disabled email notifications.


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


Override Templates/Blocks
=========================

``django-periodicals`` provides a full set of templates for displaying the data models and their relationships, searching and adding moderated links. So you can just use it right out of the box.

``django-periodicals`` defines major template blocks: ``title``, ``breadcrumbs``, ``innercontent`` and ``copyright`` that you can incorporate into your own ``base.html``. There are numerous CSS classes and container ``divs`` to give design layout options without needing to rewrite the templates.

Here is the template inheritance diagram::

                                    /---base.html--
                              /-----               \--
                        /-----                        \-
                  /-----                                \--
               ---                                         \
      base_periodicals.html                      article_tag_detail.html
          (adds search)                          author_detail.html
               |     ---                         author_list.html
               |        \---                     link_add.html
               |            \---                 link_success.html
               |                \----            search.html
               |                     \---        tags.html
               |                         \---
               |                             \
       base_periodical.html          periodical_list.html
  (adds copyright per periodical)
               |
               |
       article_detail.html
       issue_detail.html
       issue_year.html
       links.html
       periodical_detail.html
       read_online.html
       series_detail.html
       series_list.html

You might override ``base.html`` in your existing "glue" application:

.. code-block :: bash

   $ cd myapp

   $ mkdir -p templates/periodicals/

   $ emacs base.html

You might override it as follows to use your application's base template and to discard the ``breadcrumbs`` block from the ``content`` block.

.. code-block :: html

   {% extends myapp/base.html %}

   {% block content %}
   {% block innercontent %}{% endblock innercontent %}
   {% block copyright %}{% endblock copyright %}
   {% endblock content %}


Optional Settings
=================

You can control the display format for Author, Periodical, and Issue instances and their URL slugs through the following ``settings.py`` values. The default values are shown below:

.. code-block :: python

    PERIODICALS_AUTHOR_FORMAT = "%(last_name)s, %(first_name)s %(middle_name)s %(postnomial)s"
    PERIODICALS_AUTHOR_SLUG_FORMAT = "%(last_name)s %(first_name)s %(middle_name)s %(postnomial)s"

    PERIODICALS_PERIODICAL_FORMAT = "%(name)s"
    PERIODICALS_PERIODICAL_SLUG_FORMAT = "%(name)s"

    PERIODICALS_ISSUE_FORMAT = "Vol. %(volume)s No. %(issue)s"
    PERIODICALS_ISSUE_SLUG_FORMAT = "%(volume)s %(issue)s"


Disabling Adding/Displaying Links
+++++++++++++++++++++++++++++++++

By default visitors can add moderated links to each Issue or Article. Once approved via the admin they are displayed on the appropriate Issue/Article page. To disable this feature and the sections within pages displaying links add this to ``settings.py``:

.. code-block :: python

   PERIODICALS_LINKS_ENABLED = False

By default when links are added an email is sent to managers configured for the Site in the Django admin. To disable this feature add this to ``settings.py``:

.. code-block :: python

   PERIODICALS_EMAIL_NOTIFY = False

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


Sitemap Support
===============

``django-periodicals`` provides sitemap.xml support via `django.contrib.sitemaps <https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/>`_.

#. Install ``django'contrib.sitemaps`` in you ``settings.py``:

.. code-block :: python

    INSTALLED_APPS = (
       'django.contrib.sitemaps',
        ...
        'haystack',
        'tagging',
        'captcha',
        'periodicals',
    )

#. In your ``urls.py`` import the ``sitemaps_at`` method from ``periodicals.sitemaps``, add the ``sitemap.xml`` regular expression and place the url location where you put the root of the periodicals application as the argument to ``sitemaps_at``:

.. code-block :: python

  from periodicals.sitemaps import sitemaps_at


  urlpatterns = patterns('',
      ...
      (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps_at('/periodicals')}),
  )
