import uuid

from django.db import models


def generate_uuid():
    return str(uuid.uuid4())


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
    priority = models.SmallIntegerField(unique=True, blank=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class TestStatus(ReadOnlyModel):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Job(models.Model):

    name = models.CharField(max_length=255, unique=False, blank=False)
    uniqueident = models.CharField(max_length=36, unique=True, blank=False,
                                   default=generate_uuid)
    timeout = models.IntegerField(default=0)
    priority = models.ForeignKey(JobPriority, null=True, blank=True)
    status = models.ForeignKey(JobStatus, null=True, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.uniqueident)

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
