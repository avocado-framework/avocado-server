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
# Copyright: Red Hat Inc. 2015
# Author: Cleber Rosa <cleber@redhat.com>

from rest_framework import routers
from rest_framework_nested import routers as nested_routers


class DefaultRouter(nested_routers.SimpleRouter, routers.DefaultRouter):

    """
    Router that combines nested and API root capabilities

    The first big chunk of functionality is the ability to nest multiple
    routers, from `rest_framework_nested`, but these routers lack the
    so called API Root feature, which the `rest_framework` has in its
    `DefaultRouter`.
    """
    pass
