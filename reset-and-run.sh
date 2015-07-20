#!/bin/bash
if [ -f avocadoserver.sqlite ]; then rm avocadoserver.sqlite; fi;
./scripts/avocado-server-manage migrate
./scripts/avocado-server-manage runserver 0.0.0.0:9405
