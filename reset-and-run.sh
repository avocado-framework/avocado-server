#!/bin/bash
if [ -f avocadoserver.sqlite ]; then rm avocadoserver.sqlite; fi;
./manage.py syncdb -v0 --noinput
./manage.py createsuperuser --username=admin --email='root@localhost.localdomain' --noinput
./manage.py changepassword admin
./manage.py runserver
