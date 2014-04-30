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
# Red Hat, Inc.
# Cleber Rosa <cleber@redhat.com>

from rest_framework import permissions

class ReadOnlyPermission(permissions.BasePermission):
    """
    Allows read-only operations from both authenticated and anonymous users
    """

    authenticated_users_only = False

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS)
