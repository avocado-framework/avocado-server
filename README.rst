avocado-server
==============

avocado-server provides a REST based interface for application to communicate with the avocado test server.

Status
------

Very early prototype and development stage. Don't exepect a functional test server here. Instead, continue to use Autotest.

Howto
-----

If you want to try it out, follow these steps.

Dependencies
~~~~~~~~~~~~

First install the following dependencies (`pip install` is your friend):

* django
* djangorestframework

Setup
~~~~~

Create the initial database by running::

$ ./manage.py syncdb -v0 --noinput

Now create the superuser (administrator)::

$ ./manage.py createsuperuser --username=admin --email='root@localhost.localdomain' --noinput

And choose a password::

$ ./manage.py changepassword admin

Running
~~~~~~~

Run::

$ ./manage.py runserver

Now open your browser at the given address, log in with your recently created credentials and explore the API.

For the impatient (or developer)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A script named ``reset-and-run.sh`` collects the manual commands listed earlier. It also resets (deletes) the database file, so be careful!
