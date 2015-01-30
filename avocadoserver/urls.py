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

from django.conf.urls import patterns, include, url
from avocadoserver import routers
from rest_framework_nested import routers as nested
import views

router = routers.DefaultRouter()
router.register(r'jobstatuses', views.JobStatusViewSet)
router.register(r'jobpriorities', views.JobPriorityViewSet)
router.register(r'teststatuses', views.TestStatusViewSet)
router.register(r'softwarecomponentkinds', views.SoftwareComponentKindViewSet)
router.register(r'softwarecomponentarches', views.SoftwareComponentArchViewSet)
router.register(r'softwarecomponents', views.SoftwareComponentViewSet)
router.register(r'linuxdistros', views.LinuxDistroViewSet)
router.register(r'testenvironments', views.TestEnvironmentViewSet)
router.register(r'jobs', views.JobViewSet)

jobs_router = nested.NestedSimpleRouter(router, r'jobs', lookup='job')
jobs_router.register(r'activities', views.JobActivityViewSet)
jobs_router.register(r'tests', views.TestViewSet)

tests_router = nested.NestedSimpleRouter(jobs_router, 'tests', lookup='test')
tests_router.register(r'activities', views.TestActivityViewSet)
tests_router.register(r'data', views.TestDataViewSet)

urlpatterns = patterns(
    '',
    url(r'^version/$', 'avocadoserver.views.version'),
    url(r'^', include(router.urls)),
    url(r'^', include(jobs_router.urls)),
    url(r'^', include(tests_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
