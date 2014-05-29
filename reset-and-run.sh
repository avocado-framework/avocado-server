#!/bin/bash
if [ -f avocadoserver.sqlite ]; then rm avocadoserver.sqlite; fi;
./scripts/avocado-server-manage syncdb -v0 --noinput
./scripts/avocado-server-manage createsuperuser --username=admin --email='root@localhost.localdomain' --noinput
./scripts/avocado-server-manage changepassword admin
./scripts/avocado-server-manage runserver 0.0.0.0:9405
