"""
This functional test assumes that a previously setup server is running. In the
future this will provision the server, and shut it down after the test has been
run.
"""

from avocado import Test
from avocado import main

import json
import requests


class api(Test):

    EMPTY_RESPONSE = {u'count': 0,
                      u'results': [],
                      u'previous': None,
                      u'next': None}

    default_params = {'base_url': 'http://127.0.0.1:9405',
                      'username': 'admin',
                      'password': '123'}

    def get(self, path, status_code=200):
        response = requests.get(self.params.get('base_url') + path,
                                auth=(self.params.get('username'),
                                      self.params.get('password')))
        if status_code is not None:
            self.assertEquals(response.status_code, status_code)
        return response

    def post(self, path, data, status_code=201):
        response = requests.post(self.params.get('base_url') + path,
                                 auth=(self.params.get('username'),
                                       self.params.get('password')),
                                 data=data)
        if status_code is not None:
            self.assertEquals(response.status_code, status_code)
        return response

    def delete(self, path):
        return requests.delete(self.params.get('base_url') + path,
                               auth=(self.params.get('username'),
                                     self.params.get('password')))

    def test_version(self):
        self.log.info('Testing that the server returns its version')
        self.get("/version/")

    def test_jobstatus_list(self):
        self.log.info('Testing that the server has preloaded job statuses')
        r = self.get("/jobstatuses/")
        json = r.json()
        self.assertEquals(json["count"], 10)
        names = [d.get("name") for d in json["results"]]
        self.assertIn("TEST_NA", names)
        self.assertIn("ABORT", names)
        self.assertIn("ERROR", names)
        self.assertIn("FAIL", names)
        self.assertIn("WARN", names)
        self.assertIn("PASS", names)
        self.assertIn("START", names)
        self.assertIn("ALERT", names)
        self.assertIn("RUNNING", names)
        self.assertIn("NOSTATUS", names)

    def test_jobstatus_noadd(self):
        self.log.info('Testing that the server does not allow adding a new job '
                      'status')
        data = {"name": "NEW_STATUS"}
        self.post("/jobstatuses/", data, 403)

    def test_teststatus_list(self):
        self.log.info('Testing that the server has preloaded test statuses')
        r = self.get("/teststatuses/")
        json = r.json()
        self.assertEquals(json["count"], 5)
        names = [d.get("name") for d in json["results"]]
        self.assertIn("PASS", names)
        self.assertIn("ERROR", names)
        self.assertIn("FAIL", names)
        self.assertIn("TEST_NA", names)
        self.assertIn("WARN", names)

    def test_teststatus_noadd(self):
        self.log.info('Testing that the server does not allow adding a new '
                      'test status')
        data = {"name": "NEW_STATUS"}
        self.post("/teststatuses/", data, 403)

    def test_softwarecomponentkind_list(self):
        self.log.info('Testing that the server has preloaded software component kinds')
        r = self.get("/softwarecomponentkinds/")
        json = r.json()
        self.assertEquals(json["count"], 1)
        names = [d.get("name") for d in json["results"]]
        self.assertIn("unknown", names)

    def test_softwarecomponentarch_list(self):
        self.log.info('Testing that the server has preloaded software component arches')
        r = self.get("/softwarecomponentarches/")
        json = r.json()
        self.assertEquals(json["count"], 1)
        names = [d.get("name") for d in json["results"]]
        self.assertIn("unknown", names)

    def test_softwarecomponent_list(self):
        self.log.info('Testing that the server responds to software component listing')
        r = self.get("/softwarecomponents/")

    def test_softwarecomponent_add(self):
        path = "/softwarecomponents/"
        self.log.info('Testing that the server adds a software component')
        r = self.get(path)
        count = r.json()["count"]

        data = {"kind": "unknown",
                "arch": "unknown",
                "name": "foobar",
                "version": "1.0",
                "release": "0",
                "checksum": "0"}
        self.post(path, data)
        r = self.get(path)
        new_count = r.json()["count"]
        self.assertEquals(new_count, count + 1)

    def test_linuxdistro_list(self):
        self.log.info('Testing that the server responds to linux distro listing')
        r = self.get("/linuxdistros/")

    def test_linuxdistro_add(self):
        path = "/linuxdistros/"
        self.log.info('Testing that the server adds a linux distro')
        r = self.get(path)
        count = r.json()["count"]

        data = {"arch": "unknown",
                "name": "avocadix",
                "release": "1",
                "version": "0"}
        self.post(path, data)
        r = self.get(path)
        new_count = r.json()["count"]
        self.assertEquals(new_count, count + 1)

    def test_linuxdistro_no_add_dup(self):
        path = "/linuxdistros/"
        self.log.info('Testing that the server does not add a duplicated linux '
                      'distro')
        r = self.get(path)
        distro = r.json()["results"][0]
        self.post(path, distro, 400)

    def test_testenvironment_empty_add(self):
        self.log.info('Testing that the server has no test environments')
        r = self.get("/testenvironments/")
        self.assertEquals(r.json(), self.EMPTY_RESPONSE)

        path = "/testenvironments/"
        self.log.info('Testing that the server adds a test environment')
        r = self.get(path)
        count = r.json()["count"]

        distro = {"distro": {"arch": "unknown",
                             "name": "unknown",
                             "release": "0",
                             "version": "0"}}
        data = json.dumps(distro)

        # Help the the server request parser by telling it we'll be
        # using json and not, say, form encoded data
        headers = {'content-type': 'application/json'}
        response = requests.post(self.params.get('base_url') + path,
                                 auth=(self.params.get('username'),
                                       self.params.get('password')),
                                 headers=headers,
                                 data=data)
        self.assertEquals(response.status_code, 201)

        r = self.get(path)
        new_count = r.json()["count"]
        self.assertEquals(new_count, count + 1)

    def test_jobs_empty(self):
        self.log.info('Testing that the server has no jobs')
        r = self.get("/jobs/")
        self.assertEquals(r.json(), self.EMPTY_RESPONSE)

    def test_jobs_add(self):
        self.log.info('Testing that a new job can be added')
        job = {u'id': u'a0a272a09d2edda895bae4d75f5aebfad6562fb0',
               u'name': u'foobar job',
               u'status': 'NOSTATUS',
               u'elapsed_time': 0.0,
               u'activities': [],
               u'tests': []}

        data = {"id": "a0a272a09d2edda895bae4d75f5aebfad6562fb0",
                "name": "foobar job",
                "status": "NOSTATUS"}
        r = self.post("/jobs/", data)
        self.assertEquals(r.json(), job)
        return r

    def test_jobs_del(self):
        self.log.info('Testing that a job can be deleted')
        jobs = self.get('/jobs/').json()
        job = jobs['results'][0]
        path = "/jobs/" + job['id'] + "/"
        self.log.debug('Deleting job using path: %s', path)
        r = self.delete(path)
        self.test_jobs_empty()

    def test_jobs_activities_empty(self):
        self.log.info('Testing that a newly added job has no activities')
        job = self.test_jobs_add().json()
        jobs_path = "/jobs/%s/" % job['id']
        activities_path = jobs_path + "activities/"
        activities = self.get(activities_path)
        self.assertEquals(activities.json(), self.EMPTY_RESPONSE)
        self.test_jobs_del()

if __name__ == '__main__':
    main()
