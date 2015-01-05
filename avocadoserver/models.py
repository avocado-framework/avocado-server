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
# Copyright: Red Hat Inc. 2014-2015
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
    timeout = models.PositiveIntegerField(default=0)
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


class SoftwareComponentKind(models.Model):

    """
    The type of software component

    This information should be determined by the system that either
    installs new software or that collects that information after the
    test is run.

    This is not named `SoftwareComponentType` because the obvious
    attribute name (type) on class SoftwareComponenet is reserved.
    """

    #: a name that describes the type of the software component, such as
    #: rpm, deb, etc
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return unicode(self.name)


class SoftwareComponentArch(models.Model):

    """
    The architecture of the software component
    """

    #: the name of a CPU architecture, such as x86_64, ppc64, etc
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return unicode(self.name)


class SoftwareComponent(models.Model):

    """
    A given software component that plays an important role in the test

    The major, minor and release fields are larger than usually will be
    needed, but can be used to represent a SHA1SUM if we're dealing
    with software build from source.

    The checksum is supposed to hold the package or main binary checksum,
    so that besides version comparison, a integrity check can be performed.

    Note: to compare software versions (newer or older than) from software
    built from a git repo, knowledge of that specific repo is needed.

    Note: the level of database normalization is kept halfway on purpose
    to give more flexibility on the composition of software components.

    Both packaged software from the distribution or 3rd party software
    installed from either packages or built for the test are considered
    valid SoftwareComponents.
    """

    #: a reference to a :class:`SoftwareComponentKind`
    kind = models.ForeignKey(SoftwareComponentKind,
                             null=False, blank=False,
                             on_delete=models.PROTECT)

    #: the name of the software component, usually the name of the software
    #: package or source code repository name
    name = models.CharField(max_length=255, null=False, blank=False)

    #: the complete version number of the software, such as `0.1.2`
    version = models.CharField(max_length=120, null=False, blank=False)

    #: the release version of the software component, such as `-2`
    release = models.CharField(max_length=120)

    #: the checksum of the package, main binary or the hash that describes
    #: the state of the source code repo from where the software component
    #: was built from. Besides comparing the version, a integrity check can
    #: also be performed.
    checksum = models.CharField(max_length=40)

    #: a software architecture that is the primary target of this software
    #: component. This is a reference to a :class:`SoftwareComponentArch`
    arch = models.ForeignKey(SoftwareComponentArch,
                             null=False, blank=False,
                             on_delete=models.PROTECT)

    class Meta:
        unique_together = (("kind", "name", "version", "release", "checksum",
                            "arch"))

    def __unicode__(self):
        return unicode(self.name)


class LinuxDistro(models.Model):

    """
    Represents a given linux distribution base version

    Usually a test system will be installed with a given distro plus other
    external software packages (in this model terminology, that would be
    software components).
    """

    #: A short name that uniquely identifies the distro. As a general rule,
    #: the name should only identify the distro and not an specific verion.
    #: The version and and release fields should be used for that
    name = models.CharField(max_length=40)

    #: The major version of the distribution, usually denoting a longer
    #: development cycle and support
    version = models.CharField(max_length=40, blank=False)

    #: The minor version of the distribution, usually denoting a collection
    #: of updates and improvements that are repackaged and released as another
    #: installable image and/or a service pack
    release = models.CharField(max_length=40, default='', blank=False)

    #: The predominant architecture of the compiled software that make up
    #: the distribution. If a given distribution ship with, say, both
    #: 32 and 64 bit versions of packages, the `arch` will most probably
    #: be the abbreviation for the 64 bit arch, since it's the most specific
    #: and probably the most predominant one.
    arch = models.CharField(max_length=40, blank=False)

    #: The complete list of :class:`SoftwareComponent` that make up the
    #: distribution. If the server side is preloaded with the software of a
    #: given distribution this will hold the complete list of software packages
    #: and a :class:`TestEnvironment` that uses this :class:`LinuxDistro` will
    #: then have a positive and negative list of :class:`SoftwareComponent`
    #: when compared to what's available on the :class:`LinuxDistro`
    available_software_components = models.ManyToManyField(SoftwareComponent)

    class Meta:
        unique_together = (("name", "version", "release", "arch"))

    def __unicode__(self):
        return unicode(self.name)


class TestEnvironment(models.Model):

    """
    Collects machine information that could determine the test result

    A test environment is a collection of the various factors present during
    a test run that can impact the test output. Since a test runs on a machine,
    this environment information may be what differentiates a test with a PASS
    from a test with a FAIL result.

    Test environments may then be compared, and the result from the comparison
    of one when a given test PASSED and one when the same test FAILED may be
    enough to pinpoint the cause of a failure.

    Currently only the Linux Distribution installed on the machine, and the
    complete list of software components make up the the test environment, but
    this can be expanded to include hardware devices, filesystems, general
    configurations, etc.
    """

    #: The :class:`LinuxDistro` detected to be installed by the host machine
    #: running the test
    distro = models.ForeignKey(LinuxDistro)

    #: The complete list of :class:`SoftwareComponent` that are detected to be
    #: installed on the machine or that were registered to be somehow installed
    #: during the previous or current test
    installed_software_components = models.ManyToManyField(SoftwareComponent)


class Test(models.Model):
    job = models.ForeignKey(Job, related_name='tests')
    tag = models.CharField(max_length=255, blank=False)
    status = models.ForeignKey(TestStatus, null=True, blank=True)
    environment = models.ForeignKey(TestEnvironment, null=True, blank=True)

    class Meta:
        unique_together = ('job', 'tag')


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
