============
Installation
============

At the command line::

    $ easy_install django-periodicals

Or, if you have virtualenvwrapper installed::

    $ pip install django-periodicals


Override Templates
==================

``django-periodicals`` provides a ``base.html`` that you will want to override to include the templates in to your existing "glue" application:

.. code-block :: bash

   $ mkdir -p myapp/templates/periodicals/

   $ emacs base.html

``django-periodicals`` defines ``title``, ``breadcrumbs``, ``innercontent`` and ``copyright`` template blocks that you can incorporate into your own base.html ``title`` and ``content`` template blocks:

.. code-block :: html

   {% extends myapp/base.html %}

   {% block breadcrumbs %}{% endblock breadcrumbs %}

   {% block content %}
   {% block innercontent %}{% endblock innercontent %}
   {% block copyright %}{% endblock copyright %}
   {% endblock content %}
