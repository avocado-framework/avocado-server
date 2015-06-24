.. _intro::

Avocado Server
==============

Avocado Server provides a REST based interface for applications to communicate with the avocado test server.
This project is in very early prototype and development stage, so don't expect a solid and mature test server here.

If you want to try it out, follow these steps.

Setup
~~~~~

First install the following dependencies (`pip install` is your friend):

* ``django``
* ``djangorestframework``
* ``drf-nested-routers``

Create the initial database by running::

   $ ./scripts/avocado-server-manage syncdb -v0 --noinput

Now create the superuser (administrator)::

   $ ./scripts/avocado-server-manage createsuperuser --username=admin --email='root@localhost.localdomain' --noinput

And choose a password::

   $ ./scripts/avocado-server-manage changepassword admin

Running
~~~~~~~

Run::

   $ ./scripts/avocado-server-manage runserver 0.0.0.0:9405

Now open your browser at the given address, log in with your recently created credentials and explore the API.

For the impatient (or developer) a script named ``reset-and-run.sh`` collects
the manual commands listed earlier. It also resets (deletes) the database file, so be careful!
