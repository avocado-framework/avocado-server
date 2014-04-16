from django.db import models

class Label(models.Model):
    """
    Tag that marks different types of objects, including hosts, users and tests
    """
    name = models.CharField(max_length=255, unique=True, blank=False)

    def __unicode__(self):
        return self.name

class Host(models.Model):
    """
    Machine that is capable of running a test job
    """
    name = models.CharField(max_length=255, unique=True, blank=False)

    #: Host is not supposed to receive new jobs, could be under mantainance or
    #: under some other manual interaction
    locked = models.BooleanField(default=False)

    labels = models.ManyToManyField(Label, blank=True)

    def __unicode__(self):
        return self.name

class Test(models.Model):
    """
    A test server knows about and that can be run on a Host as part of a Job
    """
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=255, unique=True, blank=False)
    def __unicode__(self):
        return self.name

class Profiler(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=255, unique=True, blank=False)

    def __unicode__(self):
        return self.name

class JobStatus(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class JobPriority(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)
    priority = models.SmallIntegerField(unique=True, blank=False)

    def __unicode__(self):
        return self.name


class TestStatus(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class TestResult(models.Model):
    name = models.CharField(max_length=255, blank=False)
    tag = models.CharField(max_length=255, blank=False)
    status = models.ForeignKey(TestStatus, default=0)

    def __unicode__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=255, unique=False, blank=False)
    priority = models.ForeignKey(JobPriority, blank=False)
    timeout = models.IntegerField(default=0)
    status = models.ForeignKey(JobStatus, default=0)

    test_results = models.ManyToManyField(TestResult, blank=True)

    def __unicode__(self):
        return self.name
