from django.db import models

class Label(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)

class Host(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    locked = models.BooleanField(default=False)
    labels = models.ManyToManyField(Label, blank=True)

class Test(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=255, unique=True, blank=False)

    def __unicode__(self):
        return self.name

class Profiler(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=255, unique=True, blank=False)

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

class Job(models.Model):
    priority = models.ForeignKey(JobPriority, blank=False)
    test = models.ForeignKey(Test, blank=False)
    timeout = models.IntegerField(default=0)
    status = models.ForeignKey(JobStatus, default=None)
