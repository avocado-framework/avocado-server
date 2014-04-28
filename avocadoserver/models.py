from django.db import models

class ReadOnlyModel(models.Model):
    """
    Model that doesn't allow saving or deleting objects

    Should be used for constant like definitions that are exposed to the
    world but should never be modified except in the code itself.
    """
    def save(self, *args, **kwargs):
        return

    def delete(self):
        return

    class Meta:
        abstract = True

class JobStatus(ReadOnlyModel):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class JobPriority(ReadOnlyModel):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)
    priority = models.SmallIntegerField(unique=True, blank=False)

    def __unicode__(self):
        return self.name

class TestStatus(ReadOnlyModel):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

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

class TestResult(models.Model):
    name = models.CharField(max_length=255, blank=False)
    tag = models.CharField(max_length=255, blank=False)
    status = models.ForeignKey(TestStatus, default=0)

    def __unicode__(self):
        return self.name

class Job(models.Model):
    name = models.CharField(max_length=255, unique=False, blank=False)
    unique_id = models.CharField(max_length=36, unique=True, blank=False)
    priority = models.ForeignKey(JobPriority, blank=False)
    timeout = models.IntegerField(default=0)
    status = models.ForeignKey(JobStatus, default=0)

    def __unicode__(self):
        return self.name

class JobActivity(models.Model):
    job = models.ForeignKey(Job, related_name='activities')
    activity = models.CharField(max_length=20, blank=False)
    time = models.DateTimeField()

    class Meta:
        unique_together = ('job', 'activity', 'time')

class TestActivity(models.Model):
    job = models.ForeignKey(Job, related_name='test_activities')
    test_tag = models.CharField(max_length=255, blank=False)
    activity = models.CharField(max_length=20, blank=False)
    time = models.DateTimeField()

    def __unicode__(self):
        return "%s %s at %s" % (self.test_tag, self.activity, self.time)
