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

class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Test
        fields = ('name', 'description', 'url')

class ProfilerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Profiler
        fields = ('name', 'description', 'url')

class JobSerializer(serializers.HyperlinkedModelSerializer):

    priority = serializers.SlugRelatedField(slug_field='name')
    test = serializers.SlugRelatedField(slug_field='name')
    status = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = models.Job
        fields = ('priority', 'test', 'timeout', 'status')

