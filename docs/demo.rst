.. _try-the-demo-project:

=====================
Try the Demo Project!
=====================

Follow the installation instructions described in :ref:`installing-from-github`. There is a directory called ``demo`` in the checkout directory that contains a fully functional installation.

It is designed to show how you might to configure your project to use this application.

I overrode the ``base.html`` template and added in some trivial `Twitter Bootstrap <http://getbootstrap.com/>`_ styling so the pages wouldn't be unstyled. ``django-periodicals`` does not require the use of Bootstrap.

To setup and run the demo follow these steps::

    $ cd django-periodicals
    $ virtualenv demoenv
    $ source demoenv/bin/activate
    $ pip install -r requirements-test.txt
    $ pip install Django
    $ cd demo
    $ python manage.py syncdb
    $ python manage.py loaddata demo_tagging.json
    $ python manage.py loaddata demo_periodicals.json
    $ python manage.py update_index
    $ python manage.py runserver

Then visit the demo site at http://127.0.0.1:8000/.
