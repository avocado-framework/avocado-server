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

import models

from rest_framework import serializers


class JobStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JobStatus
        fields = ('name', 'description')


class TestStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TestStatus
        fields = ('name', 'description')


class JobActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JobActivity
        fields = ('job', 'activity', 'time')


class TestStatusSerializerField(serializers.RelatedField):

    def from_native(self, data):
        try:
            obj = models.TestStatus.objects.get(name=data)
        except models.TestStatus.DoesNotExist:
            obj = None
        return obj

    def to_native(self, value):
        return "%s" % value.name


class TestActivitySerializer(serializers.ModelSerializer):

    status = TestStatusSerializerField(read_only=False, required=False)

    class Meta:
        model = models.TestActivity
        fields = ('job', 'test_tag', 'activity', 'time', 'status')


class JobPrioritySerializerField(serializers.RelatedField):

    def from_native(self, data):
        try:
            obj = models.JobPriority.objects.get(name=data)
        except models.JobPriority.DoesNotExist:
            obj = None
        return obj

    def to_native(self, value):
        if isinstance(value, models.JobPriority):
            return "%s" % value.name


class JobStatusSerializerField(serializers.RelatedField):

    def from_native(self, data):
        try:
            obj = models.JobStatus.objects.get(name=data)
        except models.JobStatus.DoesNotExist:
            obj = None
        return obj

    def to_native(self, value):
        return "%s" % value.name


class JobSerializer(serializers.ModelSerializer):

    priority = JobPrioritySerializerField(read_only=False, required=False)
    status = JobStatusSerializerField(read_only=False, required=False)

    activities = JobActivitySerializer(many=True, read_only=True)
    test_activities = TestActivitySerializer(many=True, read_only=True)

    def validate_timeout(self, attrs, source):
        '''
        Correct negative timeouts, since they don't make sense
        '''
        attrs['timeout'] = max(attrs['timeout'], 0)
        return attrs

    class Meta:
        model = models.Job
        fields = ('id', 'name', 'uniqueident', 'timeout', 'priority', 'status',
                  'activities', 'test_activities')
        read_only_fields = ('id', )
