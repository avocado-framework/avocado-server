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

import django.db

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


if __name__ == '__main__':
    unittest.main()
