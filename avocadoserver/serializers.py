import models

from rest_framework import serializers

class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Label
        fields = ('name', )

class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Host
        fields = ('name', 'locked', 'labels')

class TestStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TestStatus
        fields = ('name', 'description')

class TestResultSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = models.TestResult
        fields = ('name', 'tag', 'status')

class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Test
        fields = ('name', 'description', 'url')

class ProfilerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Profiler
        fields = ('name', 'description', 'url')


class TestStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TestStatus
        fields = ('name', 'description')


class JobStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.JobStatus
        fields = ('name', 'description')


class JobSerializer(serializers.HyperlinkedModelSerializer):

    priority = serializers.SlugRelatedField(slug_field='name')
    status = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = models.Job
        fields = ('name', 'priority', 'timeout', 'status')

