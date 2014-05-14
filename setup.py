#!/usr/bin/python
#
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
# Copyright: Red Hat Inc. 2013-2014
# Author: Cleber Rosa <cleber@redhat.com>

# pylint: disable=E0611
from distutils.core import setup

import avocadoserver.version

setup(name='avocadoserver',
      version=avocadoserver.version.VERSION,
      description='Avocado Test Framework Server',
      author='Cleber Rosa',
      author_email='cleber@redhat.com',
      url='http://github.com/avocadoframework/avocado-server',
      packages=['avocadoserver', ],
      package_data={'avocadoserver': ['fixtures/initial_data.json']},
      scripts=['scripts/avocado-server-manage'])
