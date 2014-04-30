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
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


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

    @action(methods=['POST'])
    def activity(self, request, pk=None):
        job_activity = serializers.JobActivitySerializer(data=request.DATA)
        if job_activity.is_valid():
            job_activity.save()
            return Response({'status': 'job activity added'})
        else:
            return Response(job_activity.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'])
    def test_activity(self, request, pk=None):
        test_activity = serializers.TestActivitySerializer(data=request.DATA)
        if test_activity.is_valid():
            test_activity.save()
            return Response({'status': 'test activity added'})
        else:
            return Response(test_activity.errors,
                            status=status.HTTP_400_BAD_REQUEST)
