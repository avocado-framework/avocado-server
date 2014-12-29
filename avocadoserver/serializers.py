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


#
# Serializer Fields: deal with the individual fields that need special
# behaviour when used on Serializer
#

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


class TestStatusSerializerField(serializers.RelatedField):

    def from_native(self, data):
        try:
            obj = models.TestStatus.objects.get(name=data)
        except models.TestStatus.DoesNotExist:
            obj = None
        return obj

    def to_native(self, value):
        return "%s" % value.name


#
# Serializers: deal wit the serialization of complete records. Can make use
# of field serializers defined earlier
#

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


class TestActivitySerializer(serializers.ModelSerializer):

    status = TestStatusSerializerField(read_only=False, required=False)

    class Meta:
        model = models.TestActivity
        fields = ('test', 'activity', 'time', 'status')


class TestDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TestData
        fields = ('test', 'category', 'key', 'value')


class TestSerializer(serializers.ModelSerializer):

    status = TestStatusSerializerField(read_only=False, required=False)

    class Meta:
        model = models.Test
        fields = ('id', 'job', 'tag', 'status')
        read_only_fields = ('id', )


class JobSerializer(serializers.ModelSerializer):

    priority = JobPrioritySerializerField(read_only=False, required=False)
    status = JobStatusSerializerField(read_only=False, required=False)

    # pylint: disable=E1123
    activities = JobActivitySerializer(many=True, read_only=True)
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = models.Job
        fields = ('id', 'name', 'timeout', 'priority', 'status',
                  'activities', 'tests')
