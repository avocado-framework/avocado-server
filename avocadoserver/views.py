from avocadoserver import models, serializers
from rest_framework import viewsets

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
