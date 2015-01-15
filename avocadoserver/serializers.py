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


class JobPrioritySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JobPriority
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

    status = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.TestStatus.objects.all())

    class Meta:
        model = models.TestActivity
        fields = ('test', 'activity', 'time', 'status')


class TestDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TestData
        fields = ('test', 'category', 'key', 'value')


class TestSerializer(serializers.ModelSerializer):

    status = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.TestStatus.objects.all())

    class Meta:
        model = models.Test
        fields = ('id', 'job', 'tag', 'status')
        read_only_fields = ('id', )


class JobSerializer(serializers.ModelSerializer):

    priority = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.JobPriority.objects.all())

    status = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.JobStatus.objects.all())

    # pylint: disable=E1123
    activities = JobActivitySerializer(many=True, read_only=True)
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = models.Job
        fields = ('id', 'name', 'timeout', 'priority', 'status',
                  'activities', 'tests')


class SoftwareComponentKindSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SoftwareComponentKind
        fields = ("name",)


class SoftwareComponentArchSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SoftwareComponentArch
        fields = ("name",)
