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

import re
import uuid

from django.db import models

from job_id import create_unique_job_id


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
    id = models.CharField(max_length=40, unique=True, blank=False, primary_key=True,
                          default=create_unique_job_id)
    name = models.CharField(max_length=255, unique=False, blank=True, null=True)
    timeout = models.IntegerField(default=0)
    priority = models.ForeignKey(JobPriority, null=True, blank=True)
    status = models.ForeignKey(JobStatus, null=True, blank=True)

    def __unicode__(self):
        if self.name:
            return "%s (%s)" % (self.id, self.name)
        else:
            return self.id


class JobActivity(models.Model):
    job = models.ForeignKey(Job, related_name='activities')
    activity = models.CharField(max_length=20, blank=False)
    time = models.DateTimeField()

    class Meta:
        unique_together = ('job', 'activity', 'time')


class Test(models.Model):
    job = models.ForeignKey(Job, related_name='tests')
    tag = models.CharField(max_length=255, blank=False)
    status = models.ForeignKey(TestStatus, null=True, blank=True)

    class Meta:
        unique_together = ('job', 'tag', 'status')


class TestData(models.Model):
    test = models.ForeignKey(Test, related_name='datum')
    category = models.CharField(max_length=255, blank=False)
    key = models.CharField(max_length=255, blank=False)
    value = models.BinaryField(null=True, blank=True)

    class Meta:
        unique_together = ('test', 'category', 'key')


class TestActivity(models.Model):
    test = models.ForeignKey(Test, related_name='activities')
    activity = models.CharField(max_length=20, blank=False)
    time = models.DateTimeField()
    status = models.ForeignKey(TestStatus, null=True, blank=True)

    def __unicode__(self):
        return "%s %s at %s" % (self.test, self.activity, self.time)

    class Meta:
        unique_together = ('test', 'activity', 'time', 'status')
