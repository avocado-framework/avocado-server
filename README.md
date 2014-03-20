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

Create the database by running:

``$ ./manage.py syncdb``

Please create the `admin` user and set a password.

Running
~~~~~~~

Run:

``$ ./manage.py runserver``

Now open your browser at the given address, log in with your recently created credentials and explore the API.
