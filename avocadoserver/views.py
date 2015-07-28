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

from django.http import Http404
from django.utils import six
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import exception_handler as _exception_handler

from . import models
from . import serializers
from . import permissions
from .version import VERSION


class Http409(Exception):
    pass


def exception_handler(exc, context):
    if isinstance(exc, Http409):
        msg = _('Conflict.')
        data = {'detail': six.text_type(msg)}
        return Response(data, status=status.HTTP_409_CONFLICT)
    else:
        return _exception_handler(exc, context)


@api_view(['GET'])
@permission_classes((permissions.ReadOnlyPermission,))
def version(request, format=None):
    """
    Returns the version of the running avocado server as JSON
    """
    return Response({'version': VERSION})


class TestStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TestStatus.objects.all()
    serializer_class = serializers.TestStatusSerializer
    permission_classes = (permissions.ReadOnlyPermission, )


class JobStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.JobStatus.objects.all()
    serializer_class = serializers.JobStatusSerializer
    permission_classes = (permissions.ReadOnlyPermission, )


class JobViewSet(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('time', 'status', 'elapsed_time', 'description',)

    def get_object(self):
        try:
            obj = models.Job.objects.get(pk=self.kwargs['pk'])
            if obj is None:
                raise Http404
            else:
                return obj
        except MultipleObjectsReturned:
            raise Http409

    @list_route()
    def summary(self, request):
        total = models.Job.objects.count()
        passed = models.Job.objects.filter(status__name='PASS').count()
        failed = models.Job.objects.filter(Q(status__name='FAIL') |
                                           Q(status__name='ERROR')).count()
        other = total - (passed + failed)
        return Response({'passed': passed, 'failed': failed, 'other': other})

    @detail_route(methods=['post'])
    def activity(self, request, *args, **kwargs):
        # pylint: disable=E1123
        job_activity = serializers.JobActivitySerializer(data=request.DATA)
        if job_activity.is_valid():
            job_activity.save()
            return Response({'status': 'job activity added'})
        else:
            return Response(job_activity.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def test_activity(self, request, *args, **kwargs):
        # pylint: disable=E1123
        test_activity = serializers.TestActivitySerializer(data=request.DATA)
        if test_activity.is_valid():
            test_activity.save()
            return Response({'status': 'test activity added'})
        else:
            return Response(test_activity.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class JobActivityViewSet(viewsets.ModelViewSet):
    queryset = models.JobActivity.objects.all()
    serializer_class = serializers.JobActivitySerializer

    def create(self, request, job_pk):
        try:
            job = models.Job.objects.get(pk=job_pk)
        except models.Job.DoesNotExist:
            raise Http404

        job_activity = models.JobActivity.objects.create(
            job=job,
            activity=request.DATA['activity'],
            time=request.DATA['time'])

        job_activity.save()
        return Response({'status': 'job activity added'})


class TestViewSet(viewsets.ModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = serializers.TestSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('tag', 'status',)

    @list_route()
    def summary(self, request, job_pk):
        tests = models.Job.objects.get(pk=job_pk).tests
        total = tests.count()
        passed = tests.filter(status__name='PASS').count()
        failed = tests.filter(Q(status__name='FAIL') |
                              Q(status__name='ERROR')).count()
        other = total - (passed + failed)
        return Response({"passed": passed,
                         "failed": failed,
                         "other": other})

    def create(self, request, job_pk):
        try:
            job = models.Job.objects.get(pk=job_pk)
        except models.Job.DoesNotExist:
            raise Http404

        try:
            teststatus = models.TestStatus.objects.get(name=request.DATA['status'])
        except models.TestStatus.DoesNotExist:
            raise Http404

        test = models.Test.objects.create(job=job,
                                          status=teststatus,
                                          tag=request.DATA['tag'])
        test.save()
        return Response({'status': 'test added'})


class TestActivityViewSet(viewsets.ModelViewSet):
    queryset = models.TestActivity.objects.all()
    serializer_class = serializers.TestActivitySerializer

    def create(self, request, job_pk, test_pk):
        try:
            test = models.Test.objects.get(pk=test_pk)
        except models.Test.DoesNotExist:
            raise Http404

        status_name = request.DATA.get('status', None)
        if status_name is not None:
            try:
                status = models.TestStatus.objects.get(name=status_name)
            except models.TestStatus.DoesNotExist:
                raise Http404
        else:
            status = None

        test_activity = models.TestActivity.objects.create(
            test=test,
            activity=request.DATA['activity'],
            time=request.DATA['time'],
            status=status)

        test_activity.save()
        return Response({'status': 'test activity added'})


class TestDataViewSet(viewsets.ModelViewSet):
    queryset = models.TestData.objects.all()
    serializer_class = serializers.TestDataSerializer

    def create(self, request, job_pk, test_pk):
        try:
            test = models.Test.objects.get(pk=test_pk)
        except models.Test.DoesNotExist:
            raise Http404

        test_data = models.TestData.objects.create(
            test=test,
            category=request.DATA.get('category', 'default'),
            key=request.DATA['key'],
            value=request.DATA['value'])

        test_data.save()
        return Response({'status': 'test data added'})


class SoftwareComponentKindViewSet(viewsets.ModelViewSet):
    queryset = models.SoftwareComponentKind.objects.all()
    serializer_class = serializers.SoftwareComponentKindSerializer


class SoftwareComponentArchViewSet(viewsets.ModelViewSet):
    queryset = models.SoftwareComponentArch.objects.all()
    serializer_class = serializers.SoftwareComponentArchSerializer


class SoftwareComponentViewSet(viewsets.ModelViewSet):
    queryset = models.SoftwareComponent.objects.all()
    serializer_class = serializers.SoftwareComponentSerializer


class LinuxDistroViewSet(viewsets.ModelViewSet):
    queryset = models.LinuxDistro.objects.all()
    serializer_class = serializers.LinuxDistroSerializer


class TestEnvironmentViewSet(viewsets.ModelViewSet):
    queryset = models.TestEnvironment.objects.all()
    serializer_class = serializers.TestEnvironmentSerializer
