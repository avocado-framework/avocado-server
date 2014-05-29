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


jobs/<id>/testcount/
~~~~~~~~~~~~~~~~~~~~

This is a utility API that returns the number of tests that are part of the given job. Calling `/jobs/1/testcount/` GETs you::

   {"testcount": 3}

It's intended to be as simple as that.


jobs/<id>/passrate/
~~~~~~~~~~~~~~~~~~~

This is another utility API that returns the passrate for the tests that are part of the given job. Calling `/jobs/1/passrate/` GETs you::

   {"passrate": 66.67}

This job has had two tests that PASSed and one that FAILed. The rate gets rounded to two decimal digits.


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

jobs/<id>/activities/
~~~~~~~~~~~~~~~~~~~~~

This API accepts receiving job activity data, that is, POSTing new activities, and also listing (via GET) the activities of a job. Calling `/jobs/1/activities/` can GET you::

   {"count": 1, "next": null, "previous": null, "results":
      [{"job": 1, "activity": "JOB_START", "time": "2013-05-02T04:59:59Z"}]

Later, say that the job finishes running, the server may be updated by a client such as::

   $ curl -u admin:123 -H "Content-Type: application/json" \
     -d '{"activity": "JOB_FINISHED", "time": "2013-05-02 00:01:01"}' \
     http://localhost:9405/jobs/1/activities/
