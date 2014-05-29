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

   $ ./scripts/avocado-server-manage runserver

Now open your browser at the given address, log in with your recently created credentials and explore the API.

For the impatient (or developer)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A script named ``reset-and-run.sh`` collects the manual commands listed earlier. It also resets (deletes) the database file, so be careful!


REST API Usage
--------------

This is a basic description of the API exposed via REST. All the following subsections have as title the URI suffix they are available at.

jobstatuses
~~~~~~~~~~~

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


teststatuses
~~~~~~~~~~~~

This will list the known test statuses. Please note that a given job can have multiple tests, each one with a different result status.

Usage example::

   $ curl http://127.0.0.1:8000/teststatuses/

Sample (beautified) JSON result::

   {"count": 5, "next": null, "previous": null, "results":
      [{"name": "PASS", "description": "Test succeeded"},
       {"name": "ERROR", "description": "Test had an error"},
       {"name": "FAIL", "description": "Test failed"},
       {"name": "TEST_NA", "description": "Test was skipped"},
       {"name": "WARN", "description": "Test generated warnings"}]
   }


jobs
~~~~

This presents the view of jobs the server has. Jobs currently are run first on a standalone avocado environment, and then have their results pushed to a server.

In the future, the avocado-server will also offer job submission features, and both jobs submitted through the server and run on a standalone avocado environment should not differ with regards to information and its structure.

One point that proves that is a job unique identification number, a `uuid`, that gets created on the server if no one is provided (assuming a job submitted through the server) or when run in the standalone avocado server (with the `--journal` plugin activated).

Usage example (requires authentication)::

   $ curl -u admin:password http://127.0.0.1:8000/jobs/

Sample (beautified) JSON result::

   {"count": 1, "next": null, "previous": null, "results":
      [{"id": 1,
        "name": "Sleeptest",
        "uniqueident": "5e31e612-f08e-4acf-a1a1-7c53f691546d",
        "timeout": 0,
        "priority": null,
        "status": null,
        "activities": [],
        "test_activities":
           [{"job": 1,
             "test_tag": "sleeptest.1",
             "activity": "STARTED", "time": "2014-05-15T16:58:01.276Z",
             "status": null},
            {"job": 1,
             "test_tag": "sleeptest.1",
              "activity": "ENDED", "time": "2014-05-15T16:58:01.297Z",
              "status": "PASS"}]
      }]
   }

Here you can see a couple of noteworthy information, including the job internal automatic incremental identification (`1`), its name (`Sleeptest`), its unique identification number (`5e31e612-f08e-4acf-a1a1-7c53f691546d`).

Under `activities`, there could be a list of records of job events, such as job setup and clean up steps execution.

Under `test_activities`, you can see different activities recorded by the test runner for a given test, including where appropriate, its `status` (or result, if you prefer to think like that).
