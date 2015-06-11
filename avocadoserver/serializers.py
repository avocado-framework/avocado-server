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

    status = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.JobStatus.objects.all())

    # pylint: disable=E1123
    activities = JobActivitySerializer(many=True, read_only=True)
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = models.Job
        fields = ('id', 'description', 'time', 'timeout', 'status',
                  'activities', 'tests')


class SoftwareComponentKindSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SoftwareComponentKind
        fields = ("name",)


class SoftwareComponentArchSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SoftwareComponentArch
        fields = ("name",)


class SoftwareComponentSerializer(serializers.ModelSerializer):

    kind = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.SoftwareComponentKind.objects.all())

    arch = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.SoftwareComponentArch.objects.all())

    class Meta:
        model = models.SoftwareComponent
        fields = ("name", "version", "release", "checksum", "kind", "arch")


class LinuxDistroSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LinuxDistro
        fields = ("name", "version", "release", "arch")


class LinuxDistroField(serializers.Field):

    def to_internal_value(self, data):
        try:
            distro = models.LinuxDistro.objects.get(name=data.get('name'),
                                                    arch=data.get('arch'),
                                                    version=data.get('version'),
                                                    release=data.get('release'))
            return distro
        except:
            self.fail('invalid', input=data)

    def to_representation(self, value):
        return {'name': value.name,
                'arch': value.arch,
                'version': value.version,
                'release': value.release}


class TestEnvironmentSerializer(serializers.ModelSerializer):

    distro = LinuxDistroField()
    installed_software_components = SoftwareComponentSerializer(many=True,
                                                                read_only=True)

    class Meta:
        model = models.TestEnvironment
        fields = ("distro", "installed_software_components")
