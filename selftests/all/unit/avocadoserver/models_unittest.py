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

    def test_job_nodescription(self):
        job = models.Job.objects.create(elapsed_time=100.0)
        self.assertEquals(job.description, None)

    def test_job_automatic_id(self):
        job = models.Job.objects.create()
        self.assertNotEquals(job.id, None)

    def test_job_automatic_id_len_40(self):
        job = models.Job.objects.create()
        self.assertEquals(len(job.id), 40)

    def test_job_default_elapsed_time(self):
        job = models.Job.objects.create()
        self.assertEquals(job.elapsed_time, 0.0)

    def test_job_add_same_id(self):
        '''
        Attempts to create two jobs with the same unique identification

        This should fail and trigger an IntegrityError
        '''
        job_1 = models.Job.objects.create()
        self.assertRaises(django.db.IntegrityError,
                          models.Job.objects.create,
                          id=job_1.id)

    def test_job_add_same_description(self):
        '''
        There are no restrictions on multiple jobs having the same description
        '''
        job_1 = models.Job.objects.create(description='same')
        job_2 = models.Job.objects.create(description='same')
        self.assertEquals(job_1.description, job_2.description)

    def test_job_activity(self):
        '''
        Adds job activity to an existing job
        '''
        job = models.Job.objects.create(description='job with activities')
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
        job = models.Job.objects.create(description='job with activities')
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        job_setup = models.JobActivity.objects.create(job=job,
                                                      activity='setup',
                                                      time=now)
        self.assertRaises(django.db.IntegrityError,
                          models.JobActivity.objects.create,
                          job=job, activity='setup', time=now)

    def test_job_add_test_activity(self):
        job = models.Job.objects.create(description='job with test activities')
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
        job = models.Job.objects.create(description='job with test data')
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

    def test_sofware_component_kind_create_delete(self):
        models.SoftwareComponentKind.objects.create(name='rpm')
        self.assertEqual(2, models.SoftwareComponentKind.objects.all().count())

        models.SoftwareComponentKind.objects.all().delete()
        self.assertEqual(0, models.SoftwareComponentKind.objects.all().count())

    def test_software_component_kind_create_duplicate(self):
        def create_kind():
            models.SoftwareComponentKind.objects.create(name='rpm')

        create_kind()
        self.assertRaises(django.db.IntegrityError, create_kind)
        models.SoftwareComponentKind.objects.all().delete()

    def test_software_component_arch_create_delete(self):
        models.SoftwareComponentArch.objects.create(name='x86_64')
        self.assertEqual(2, models.SoftwareComponentArch.objects.all().count())

        models.SoftwareComponentArch.objects.all().delete()
        self.assertEqual(0, models.SoftwareComponentArch.objects.all().count())

    def test_software_component_arch_create_duplicate(self):
        def create_arch():
            models.SoftwareComponentArch.objects.create(name='x86_64')

        create_arch()
        self.assertRaises(django.db.IntegrityError, create_arch)
        models.SoftwareComponentArch.objects.all().delete()

    def test_software_component_delete_reference(self):
        '''
        Should not be possible to delete a Software Component Arch that
        is referenced by an existing Software Component
        '''
        kind = models.SoftwareComponentKind.objects.create(name='rpm')
        kind.save()
        kind_id = kind.id

        arch = models.SoftwareComponentArch.objects.create(name='x86_64')
        arch.save()
        arch_id = arch.id

        sc = models.SoftwareComponent.objects.create(name='foo',
                                                     kind=kind,
                                                     arch=arch,
                                                     version='1.0.0')
        sc.save()
        sc_id = sc.id
        sc = models.SoftwareComponent.objects.get(pk=sc_id)

        arch = models.SoftwareComponentArch.objects.get(pk=arch_id)

        def arch_delete():
            arch.delete()

        self.assertRaises(django.db.models.ProtectedError, arch_delete)
        models.SoftwareComponent.objects.all().delete()
        models.SoftwareComponentKind.objects.all().delete()
        models.SoftwareComponentArch.objects.all().delete()

    def test_distro_create_delete(self):
        # The builtin 'unknown distro' accounts for the first count
        self.assertEqual(1, models.LinuxDistro.objects.all().count())

        models.LinuxDistro.objects.create(name='distro', version='1',
                                          release='0', arch='i386')

        self.assertEqual(2, models.LinuxDistro.objects.all().count())

        models.LinuxDistro.objects.all().delete()
        self.assertEqual(0, models.LinuxDistro.objects.all().count())

    def test_distro_create_query_arch_delete(self):
        models.LinuxDistro.objects.create(name='distro', version='1',
                                          release='0', arch='i386')
        models.LinuxDistro.objects.create(name='distro', version='1',
                                          release='1', arch='i386')
        models.LinuxDistro.objects.create(name='distro', version='1',
                                          release='0', arch='x86_64')
        models.LinuxDistro.objects.create(name='distro', version='1',
                                          release='1', arch='x86_64')

        all_count = models.LinuxDistro.objects.all().count()
        self.assertEqual(all_count, 5)
        i386_count = models.LinuxDistro.objects.filter(arch='i386').count()
        self.assertEqual(i386_count, 2)

        models.LinuxDistro.objects.get(name='distro', version='1',
                                       release='0', arch='i386').delete()
        models.LinuxDistro.objects.get(name='distro', version='1',
                                       release='1', arch='i386').delete()
        self.assertEqual(3, models.LinuxDistro.objects.all().count())

    def test_distro_create_duplicate(self):
        def create_distro():
            models.LinuxDistro.objects.create(name='distro', version='1',
                                              release='0', arch='i386')

        create_distro()
        self.assertRaises(django.db.IntegrityError, create_distro)
        models.LinuxDistro.objects.all().delete()


if __name__ == '__main__':
    unittest.main()
