#!/usr/bin/env python

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


import os
import sys
import unittest
import datetime

import django.db
from django.utils.timezone import utc

# simple magic for using scripts within a source tree
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
basedir = os.path.dirname(basedir)
if os.path.isdir(os.path.join(basedir, 'avocadoserver')):
    sys.path.append(basedir)


from avocadoserver import unittest_utils
unittest_utils.django_environment()
unittest_utils.django_db_environment()
from avocadoserver import models


class ModelsUnitests(unittest.TestCase):

    def setUp(self):
        unittest_utils.django_syncdb()

    def test_jobstatus_cannot_be_created(self):
        '''
        Tests that a new job status can not be added programmatically

        It is assumed that if a new job status is to exist, this will be
        synced between avocado and server and added to the fixture file.
        '''
        count = models.JobStatus.objects.count()

        jobstatus = models.JobStatus.objects.create(
            name='newstatus',
            description='A new test status that has no meaning')
        jobstatus.save()

        self.assertEqual(count,
                         models.JobStatus.objects.count())

    def test_teststatus_cannot_be_removed(self):
        '''
        Tests that a new test status can not be removed programmatically

        Same reasoning described on test_jobstatus_cannot_be_created().
        '''
        count = models.TestStatus.objects.count()

        teststatus = models.TestStatus.objects.get(pk=1)
        teststatus.delete()

        self.assertEqual(count,
                         models.TestStatus.objects.count())

    def test_job_unnamed(self):
        job = models.Job.objects.create(timeout=100)
        self.assertIsNone(job.name)

    def test_job_automatic_uniqueident(self):
        job = models.Job.objects.create(name='test_job_automatic_uniqueident')
        self.assertIsNotNone(job.uniqueident)

    def test_job_default_timeout(self):
        job = models.Job.objects.create()
        self.assertEquals(job.timeout, 0)

    def test_job_add_same_uniqueident(self):
        '''
        Attempts to create two jobs with the same unique identification

        This should fail and trigger an IntegrityError
        '''
        job_1 = models.Job.objects.create()
        self.assertRaises(django.db.IntegrityError,
                          models.Job.objects.create,
                          uniqueident=job_1.uniqueident)

    def test_job_add_same_name(self):
        '''
        There are no restrictions on multiple jobs having the same name
        '''
        job_1 = models.Job.objects.create(name='same')
        job_2 = models.Job.objects.create(name='same')
        self.assertEquals(job_1.name, job_2.name)

    def test_job_activity(self):
        '''
        Adds job activity to an existing job
        '''
        job = models.Job.objects.create(name='job with activities')
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        job_setup = models.JobActivity.objects.create(job=job,
                                                      activity='setup',
                                                      time=now)
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        job_cleanup = models.JobActivity.objects.create(job=job,
                                                        activity='cleanup',
                                                        time=now)

    def test_job_same_activity(self):
        '''
        Attempts to add the same activity to the same job
        '''
        job = models.Job.objects.create(name='job with activities')
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        job_setup = models.JobActivity.objects.create(job=job,
                                                      activity='setup',
                                                      time=now)
        self.assertRaises(django.db.IntegrityError,
                          models.JobActivity.objects.create,
                          job=job, activity='setup', time=now)

    def test_job_add_test_activity(self):
        job = models.Job.objects.create(name='job with test activities')
        test = models.Test.objects.create(job=job,
                                          tag='test.1')
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        test_setup_start = models.TestActivity.objects.create(
            test=test,
            activity='SETUP_START',
            time=now)
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        test_setup_end = models.TestActivity.objects.create(
            test=test,
            activity='SETUP_END',
            time=now)

    def test_job_test_data(self):
        job = models.Job.objects.create(name='job with test data')
        test = models.Test.objects.create(job=job,
                                          tag='test.2')
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        test_data = models.TestData.objects.create(
            test=test,
            category='sysinfo',
            key='cmdline',
            value=('BOOT_IMAGE=/vmlinuz-3.14.3-200.fc20.x86_64 '
                   'root=/dev/mapper/vg_x220-f19root ro rd.md=0 rd.dm=0 '
                   'vconsole.keymap=us rd.lvm.lv=vg_x220/f19root rd.luks=0'
                   'vconsole.font=latarcyrheb-sun16 rd.lvm.lv=vg_x220/swap '
                   'rhgb quiet LANG=en_US.UTF-8'))


if __name__ == '__main__':
    unittest.main()
