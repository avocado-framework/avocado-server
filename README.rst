avocado-server
==============

avocado-server provides a REST based interface for application to communicate with the avocado test server.

Status
------

Very early prototype and development stage. Don't exepect a functional test server here. Instead, continue to use Autotest.

Howto
-----

If you want to try it out, follow these steps.

Dependencies
~~~~~~~~~~~~

First install the following dependencies (`pip install` is your friend):

* django
* djangorestframework
* drf-nested-routers

Setup
~~~~~

Create the initial database by running::

   $ ./scripts/avocado-server-manage syncdb -v0 --noinput

Now create the superuser (administrator)::

   $ ./scripts/avocado-server-manage createsuperuser --username=admin --email='root@localhost.localdomain' --noinput

And choose a password::

   $ ./scripts/avocado-server-manage changepassword admin

Running
~~~~~~~

Run::

   $ ./scripts/avocado-server-manage runserver 0.0.0.0:9405

Now open your browser at the given address, log in with your recently created credentials and explore the API.

For the impatient (or developer)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A script named ``reset-and-run.sh`` collects the manual commands listed earlier. It also resets (deletes) the database file, so be careful!


REST API Usage
--------------

This is a basic description of the API exposed via REST. All the following subsections have as title the URI suffix they are available at.

version/
~~~~~~~~

The most basic information given by the server is its own version. Usage example::

   $ curl http://127.0.0.1:8000/version/

Sample result::

   {"version": "0.1.0"}


jobstatuses/
~~~~~~~~~~~~

This will list all known job statuses by the avocado server. This can be used by clients, such as the avocado scripts that interact with a server to write appropriate result values.

Usage example::

   $ curl http://127.0.0.1:8000/jobstatuses/

Sample (beautified) JSON result::

   {"count": 10, "next": null, "previous": null, "results":
      [{"name": "TEST_NA", "description": ""},
       {"name": "ABORT", "description": "Job was removed from queue before completion"},
       {"name": "ERROR", "description": ""},
       {"name": "FAIL", "description": ""},
       {"name": "WARN", "description": ""},
       {"name": "PASS", "description": "Job finished running successfull"},
       {"name": "START", "description": "Job just started running"},
       {"name": "ALERT", "description": ""},
       {"name": "RUNNING", "description": "Job is currently being executed"},
       {"name": "NOSTATUS", "description": "Job has no recognizable status"}]
   }


teststatuses/
~~~~~~~~~~~~~

This will list the known test statuses. Please note that a given job can have multiple tests, each one with a different result status.

Usage example::

   $ curl http://127.0.0.1:9405/teststatuses/

Sample (beautified) JSON result::

   {"count": 5, "next": null, "previous": null, "results":
      [{"name": "PASS", "description": "Test succeeded"},
       {"name": "ERROR", "description": "Test had an error"},
       {"name": "FAIL", "description": "Test failed"},
       {"name": "TEST_NA", "description": "Test was skipped"},
       {"name": "WARN", "description": "Test generated warnings"}]
   }


jobs/
~~~~~

This presents the view of jobs the server has. Jobs currently are run first on a standalone avocado environment, and then have their results pushed to a server.

In the future, the avocado-server will also offer job submission features, and both jobs submitted through the server and run on a standalone avocado environment should not differ with regards to information and its structure.

One point that proves that is a job unique identification number, a `uuid`, that gets created on the server if no one is provided (assuming a job submitted through the server) or when run in the standalone avocado server (with the `--journal` plugin activated).

Usage example (requires authentication)::

   $ curl -u admin:password http://127.0.0.1:9405/jobs/

Sample (beautified) JSON result::

   {"count": 1, "next": null, "previous": null, "results":
      [{"id": 1,
        "name": "Sleep, fail and sync",
        "uniqueident": "5e31e612-f08e-4acf-a1a1-7c53f691546d",
        "timeout": 0,
        "priority": null,
        "status": null,
        "activities": [],
	"tests":
	   [{"id": 3,
	     "job": 1,
	     "tag": "failtest",
	      "status": "FAIL"},

	    {"id": 1,
	     "job": 1,
	     "tag": "sleeptest",
	     "status": "PASS"},

	    {"id": 2,
	     "job": 1,
	     "tag": "synctest",
	     "status": "PASS"}]
      }]
   }

Here you can see a couple of noteworthy information, including the job internal automatic incremental identification (`1`), its name (`Sleep, fail and sync`), its unique identification number (`5e31e612-f08e-4acf-a1a1-7c53f691546d`).

Under `activities`, there could be a list of records of job events, such as job setup and clean up steps execution.

Under `tests`, you can see the tests that were recorded as part of this job.

jobs/<id>/activities/
~~~~~~~~~~~~~~~~~~~~~

This API accepts receiving job activity data, that is, POSTing new activities, and also listing (via GET) the activities of a job. Calling `/jobs/1/activities/` can GET you::

   {"count": 1, "next": null, "previous": null, "results":
      [{"job": 1, "activity": "JOB_START", "time": "2013-05-02T04:59:59Z"}]

Later, say that the job finishes running, the server may be updated by a client such as::

   $ curl -u admin:123 -H "Content-Type: application/json" \
     -d '{"activity": "JOB_FINISHED", "time": "2013-05-02 00:01:01"}' \
     http://localhost:9405/jobs/1/activities/


jobs/<id>/tests/
~~~~~~~~~~~~~~~~

This API accepts receiving test data, that is, POSTing new tests that are part of a given job, and also listing (via GET) the tests of a job. Calling `/jobs/1/tests/` GETs you::

   {"count": 3, "next": null, "previous": null, "results":
      [{"id": 1, "job": 1, "tag": "sleeptest", "status": "PASS"},
       {"id": 2, "job": 1, "tag": "synctest", "status": "PASS"},
       {"id": 3, "job": 1, "tag": "failtest", "status": "FAIL"}]
   }

To register a new test and its status for a given job you could run::

   $ curl -u admin:123 -H "Content-Type: application/json" -d '{"tag": "newtest", "status": "PASS"}' http://localhost:9405/jobs/1/tests/

The result will hopefully be::

   {"status": "test added"}

Now you can probably re-check the passrate for the same job by GETting `/jobs/1/passrate`::

   {"passrate": 75.0}

jobs/<id>/tests/<id>/activities/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add a new activity related to a test::

   $ curl -u admin:123 -H "Content-Type: application/json" \
     -d '{"activity": "TEST_STARTED", "time": "2013-05-02 00:00:01"}' \
     http://localhost:9405/jobs/1/tests/1/activities/

The result will hopefully be::

   {"status": "test activity added"}

Now suppose that the same test has finished, but FAILed. This could be notified to the server by running::

   $ curl -u admin:123 -H "Content-Type: application/json" \
     -d '{"activity": "TEST_ENDED", "time": "2013-05-02 00:00:04", "status": "FAIL"}' \
     http://localhost:9405/jobs/1/tests/1/activities/

The result will hopefully be::

   {"status": "test activity added"}

Now you can see all that happenned to test 1, part of job 1, by GETting `/jobs/1/tests/1/activities/`::

   {"count": 2, "next": null, "previous": null, "results": [
    {"test": 1, "activity": "TEST_STARTED", "time": "2013-05-02T05:00:01Z", "status": null},
    {"test": 1, "activity": "TEST_ENDED", "time": "2013-05-02T05:00:04Z", "status": "FAIL"}]
   }


/jobs/<id>/tests/<id>/data/
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests also generate data that usually needs to be preserved. The avocado server uses a free form approach to test data. Each test data should be marked with a given `category`, which is also free form.

One example: the avocado test runner includes the `sysinfo` plugin, which gathers some useful information about the system where the test is running on. That data is usually small, and wouldn't hurt to be loaded to the database itself. To do that, we could run::

   $ curl -u admin:123 -H "Content-Type: application/json" \
     -d '{"category": "sysinfo",
          "key": "cmdline",
          "value": "BOOT_IMAGE=/vmlinuz-3.14.3-200.fc20.x86_64 root=/dev/mapper/vg_x220-f19root ro rd.md=0 rd.dm=0 vconsole.keymap=us rd.lvm.lv=vg_x220/f19root rd.luks=0 vconsole.font=latarcyrheb-sun16 rd.lvm.lv=vg_x220/swap rhgb quiet LANG=en_US.UTF-8"}' \
     http://localhost:9405/jobs/1/tests/1/data/

And get::

   {"status": "test data added"}

But for large log files, which are best kept on the filesystem, we may simply record their relative path::

   $ curl -u admin:123 -H "Content-Type: application/json" \
     -d '{"category": "log_file_path",
          "key": "debug.log",
          "value": ""}' \
     http://localhost:9405/jobs/1/tests/1/data/

And get::

   {"status": "test data added"}
