from avocadoserver import models, serializers, permissions
from rest_framework import viewsets

class TestStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TestStatus.objects.all()
    serializer_class = serializers.TestStatusSerializer
    permission_classes = (permissions.ReadOnlyPermission, )

class JobStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.JobStatus.objects.all()
    serializer_class = serializers.JobStatusSerializer
    permission_classes = (permissions.ReadOnlyPermission, )

class LabelViewSet(viewsets.ModelViewSet):
    queryset = models.Label.objects.all()
    serializer_class = serializers.LabelSerializer

class HostViewSet(viewsets.ModelViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = serializers.TestSerializer

class ProfilerViewSet(viewsets.ModelViewSet):
    queryset = models.Profiler.objects.all()
    serializer_class = serializers.ProfilerSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
