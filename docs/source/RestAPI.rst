.. _rest_api:

=======================
Avocado Server REST API
=======================

Welcome to the Avocado Server REST API documentation. 

All examples here are pretty formatted, so the JSON output may look different,
but it doesn't have any special meaning when the data is parsed.


Pagination
==========

By default, every request returns 10 elements, more results may be returned
by means of pagination.  To select a specific page, pass the query string
argument ``page=NUMBER``, where ``NUMBER`` is an integer greater than zero.

Here is the general response for data returned with pagination::

	{
	    "count"    : NUMBER,
	    "next"     : "URL" or null,
	    "previous" : "URL" or null,
	    "results"  : [ ... ],
	}

The attributes are:

* ``count`` the number of elements retrieved.
* ``next`` URL to retrieve the next elements (next page).
* ``previous`` URL to retrieve the previous elements (previous page).
* ``results`` an array of actual data (payload).


Ordering results
================

To select one or more attributes to order the results, pass the
query string argument ``ordering=FIELD`` or
``ordering=FIELD1,FIELD2,...,FIELDN``. Using the prefix ``-`` to
any field, will reverse the order for that field.

Only the fields for Job and Test results can be selected for ordering.


Errors
======

* If the URL is not found (it is not a recognized API name), the server will
  return HTTP ``404`` (NOT FOUND) with a HTML transcription of the error message.
* If a page number is out of range, the server will return HTTP ``404``
  (NOT FOUND) with JSON result ``{"detail":"Not found"}``.


REST API
========

/
---

Get API parameters for using within Avocado Server.

Expected result::

	{
	    "NAME1" : "URL1",
	    "NAME2" : "URL2",
	    ...
	    "NAMEN" : "URLN"
	}

Usage example::

	$ curl  http://localhost:9405/

Sample result::

	{
	    "jobstatuses": "http://localhost:9405/jobstatuses/",
	    "teststatuses": "http://localhost:9405/teststatuses/",
	    "softwarecomponentkinds": "http://localhost:9405/softwarecomponentkinds/",
	    "softwarecomponentarches": "http://localhost:9405/softwarecomponentarches/",
	    "softwarecomponents": "http://localhost:9405/softwarecomponents/",
	    "linuxdistros": "http://localhost:9405/linuxdistros/",
	    "testenvironments": "http://localhost:9405/testenvironments/",
	    "jobs": "http://localhost:9405/jobs/"
	}

/version/
---------

Get version of the running Avocado Server.

The most basic information given by the server is its own version,
so you can use it as a simple functional test.

Expected result::

	{ "version" : "MAJOR.MINOR.REVISION" }

Usage example::

	$ curl http://127.0.0.1:9405/version/

Sample result::

	{"version":"0.25.0"}

/jobs/
------

Get job results.

This presents the view of jobs the server has. Jobs currently are run first on
a standalone avocado environment, and then have their results pushed to a server.

In the future, the Avocado Server will also offer job submission features,
and both jobs submitted through the server and run on a standalone avocado
environment should not differ with regards to information and its structure.

One point that proves that is a job unique identification number, a `uuid`,
that gets created on the server if no one is provided (assuming a job
submitted through the server) or when run in the standalone
Avocado Server (with the `--journal` plugin activated).

Expected result::

	{
	    "count"    : NUMBER,
	    "next"     : "URL" or null,
	    "previous" : "URL" or null,
	    "results"  : [
	        {
		    "id"           : "JOB_ID"
		    "description"  : "DESCRIPTION",
		    "time"         : "ISO-8601 TIME",
		    "elapsed_time" : SECONDS_FLOAT, 
		    "status"       : "JOB STATUS",
		    "activities"   : [ TESTACTIVITY1, ... ]
		    "tests"        : [ TESTRESULT1, ... ]
		},
		... more ...
	    ]
	}

Note: if you want to get the latest job results, use ``/jobs/?ordering=-time``.

Usage example::

	$ curl http://127.0.0.1:9405/jobs/

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

Here you can see a couple of noteworthy information, including the job
internal automatic incremental identification (`1`), its name (`Sleep, fail and sync`),
its unique identification number (`5e31e612-f08e-4acf-a1a1-7c53f691546d`).

Under `activities`, there could be a list of records of job events, such as
job setup and clean up steps execution.

Under `tests`, you can see the tests that were recorded as part of this job.

/jobs/*job_id*/
---------------

Get job result for the specific job ``job_id``.

Expected result::

	{
	    "id"           : "JOB_ID"
	    "description"  : "DESCRIPTION",
	    "time"         : "ISO-8601 TIME",
	    "elapsed_time" : SECONDS_FLOAT, 
	    "status"       : "JOB STATUS",
	    "activities"   : [ TESTACTIVITY1, ... ]
	    "tests"        : [ TESTRESULT1, ... ]
	}

/jobs/*job_id*/activities/
--------------------------

Get activities for the specific job ``job_id``.

This API accepts receiving job activity data, that is, POSTing new activities,
and also listing (via GET) the activities of a job. Calling `/jobs/1/activities/` can GET you::

	{"count": 1, "next": null, "previous": null, "results":
	   [{"job": 1, "activity": "JOB_START", "time": "2013-05-02T04:59:59Z"}]

Later, say that the job finishes running, the server may be updated by a client such as::

	$ curl -u admin:123 -H "Content-Type: application/json" \
	  -d '{"activity": "JOB_FINISHED", "time": "2013-05-02 00:01:01"}' \
	  http://localhost:9405/jobs/1/activities/

/jobs/*job_id*/tests/
---------------------

Get test results for the specific job ``job_id``.

This API accepts receiving test data, that is, POSTing new tests that are
part of a given job, and also listing (via GET) the tests of a job.

Expected result::

	{
	    "count"    : NUMBER,
	    "next"     : "URL" or null,
	    "previous" : "URL" or null,
	    "results"  : [
		{
		    "id"     : NUMBER,
		    "job"    : "JOB_ID",
		    "tag"    : "STRING",
		    "status" : "STRING"
		},
		... more ...
	    ]
	}

Calling `/jobs/1/tests/` GETs you::

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

/jobs/*job_id*/tests/*test_id*/
-------------------------------

Get test result for the specific``test_id`` related to job ``job_id``.

Expected result::

	{
	    "id"     : NUMBER,
	    "job"    : "JOB_ID",
	    "tag"    : "STRING",
	    "status" : "STRING"
	}

/jobs/*job_id*/tests/*test_id*/activities/
------------------------------------------

Get test activities for the specific test ``test_id`` related to job ``job_id``.

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

Now you can see all that happened to test 1, part of job 1, by GETting `/jobs/1/tests/1/activities/`::

	{"count": 2, "next": null, "previous": null, "results": [
	 {"test": 1, "activity": "TEST_STARTED", "time": "2013-05-02T05:00:01Z", "status": null},
	 {"test": 1, "activity": "TEST_ENDED", "time": "2013-05-02T05:00:04Z", "status": "FAIL"}]
	}

/jobs/*job_id*/tests/*test_id*/data/
------------------------------------

Get test data for the specific test ``test_id`` related to job ``job_id``.

Tests also generate data that usually needs to be preserved. The Avocado Server
uses a free form approach to test data. Each test data should be marked
with a given `category`, which is also free form.

One example: the avocado test runner includes the `sysinfo` plugin, which
gathers some useful information about the system where the test is running on.
That data is usually small, and wouldn't hurt to be loaded to the database itself.
To do that, we could run::

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


/jobstatuses/
-------------

Get the list of allowed job status.

This will list all known job statuses by the Avocado Server.
This can be used by clients, such as the Avocado scripts that interact
with a server to write appropriate result values.

Expected result::

	{
	    "count"    : NUMBER,
	    "next"     : "URL" or null,
	    "previous" : "URL" or null,
	    "results"  : [
	    	{
		    "name" : "STRING",
		    "description" : "STRING"
		},
		... more ...
	    ]
	}

Usage example::

	$ curl http://127.0.0.1:9405/jobstatuses/

Sample (beautified) JSON result::

	{
	    "count": 10,
	    "next": null,
	    "previous": null,
	    "results": [
		{
		    "name": "TEST_NA",
		    "description": ""
		},
		{
		    "name": "ABORT",
		    "description": "Job was removed from queue before completion"
		},
		{
		    "name": "ERROR",
		    "description": ""
		},
		{
		    "name": "FAIL",
		    "description": ""
		},
		{
		    "name": "WARN",
		    "description": ""
		},
		{
		    "name": "PASS",
		    "description": "Job finished running successfull"
		},
		{
		    "name": "START",
		    "description": "Job just started running"
		},
		{
		    "name": "ALERT",
		    "description": ""
		},
		{
		    "name": "RUNNING",
		    "description": "Job is currently being executed"
		},
		{
		    "name": "NOSTATUS",
		    "description": "Job has no recognizable status"
		}
	    ]
	}

/teststatuses/
--------------

Get the list of allowed test status.

This will list the known test statuses. Please note that a given job can
have multiple tests, each one with a different result status.

Expected result::

	{
	    "count"    : NUMBER,
	    "next"     : "URL" or null,
	    "previous" : "URL" or null,
	    "results"  : [
		{
		    "name" : "STRING",
		    "description" : "STRING"
		},
		... more ...
	    ]
	}

Usage example::

	$ curl http://127.0.0.1:9405/teststatuses/

Sample (beautified) JSON result::

	{
	    "count": 5,
	    "next": null,
	    "previous": null,
	    "results": [
		{
		    "name": "PASS",
		    "description": "Test succeeded"
		},
		{
		    "name": "ERROR",
		    "description": "Test had an error"
		},
		{
		    "name": "FAIL",
		    "description": "Test failed"
		},
		{
		    "name": "TEST_NA",
		    "description": "Test was skipped"
		},
		{
		    "name": "WARN",
		    "description": "Test generated warnings"
		}
	    ]
	}
