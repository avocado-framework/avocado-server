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
         fields = ('activity', 'time')

class TestActivitySerializer(serializers.ModelSerializer):
     class Meta:
         model = models.TestActivity
         fields = ('test_tag', 'activity', 'time')

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
