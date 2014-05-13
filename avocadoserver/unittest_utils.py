# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: Red Hat Inc. 2014
# Author: Cleber Rosa <cleber@redhat.com>

import os

from django.conf import settings
from django.core import management


def django_environment():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avocadoserver.settings")


def django_db_environment():
    default = settings.DATABASES['default']
    default['ENGINE'] = ('django.db.backends.sqlite3')
    default['NAME'] = ':memory:'


def django_syncdb():
    management.call_command('syncdb', verbosity=0, interactive=False)
