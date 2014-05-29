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

from avocadoserver import models, serializers, permissions
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, link


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

    def retrieve(self, request, pk):
        self.object = self.get_object(pk)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    def get_object(self, pk):
        if models.Job.UNIQUEIDENT_RE.match(pk):
            return self.get_object_by_uniqueident(pk)
        else:
            return self.get_object_by_pk(pk)
        return self.object

    def get_object_by_pk(self, pk):
        try:
            return models.Job.objects.get(pk=pk)
        except models.Job.DoesNotExist:
            raise Http404

    def get_object_by_uniqueident(self, uniqueident):
        try:
            return models.Job.objects.get(uniqueident=uniqueident)
        except models.Job.DoesNotExist:
            raise Http404

    @link()
    def testcount(self, request, pk):
        test_count = models.Test.objects.filter(job_id=pk).count()
        return Response({'testcount': test_count})

    @link()
    def passrate(self, request, pk):
        test_count = models.Test.objects.filter(job_id=pk).count()
        if test_count == 0:
            return Response({'passrate': 0})

        test_status_success = models.TestStatus.objects.get(name='PASS')
        test_count_pass = models.Test.objects.filter(job_id=pk,
                                                     status=test_status_success).count()

        rate = round((float(test_count_pass) / float(test_count)) * 100, 2)
        return Response({'passrate': rate})

    @action(methods=['POST'])
    def activity(self, request, pk=None):
        # pylint: disable=E1123
        job_activity = serializers.JobActivitySerializer(data=request.DATA)
        if job_activity.is_valid():
            job_activity.save()
            return Response({'status': 'job activity added'})
        else:
            return Response(job_activity.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'])
    def test_activity(self, request, pk=None):
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
