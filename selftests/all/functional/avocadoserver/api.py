"""
This functional test assumes that a previously setup server is running. In the
future this will provision the server, and shut it down after the test has been
run.
"""

from avocado import test

import requests


class api(test.Test):

    default_params = {'base_url': 'http://127.0.0.1:9405',
                      'username': 'admin',
                      'password': '123'}

    def get(self, path, status_code=200):
        response = requests.get(self.params.base_url + path,
                                auth=(self.params.username,
                                      self.params.password))
        if status_code is not None:
            self.assertEquals(response.status_code, status_code)
        return response

    def post(self, path, data, status_code=201):
        response = requests.post(self.params.base_url + path,
                                 auth=(self.params.username,
                                       self.params.password),
                                 data=data)
        if status_code is not None:
            self.assertEquals(response.status_code, status_code)
        return response

    def delete(self, path):
        return requests.delete(self.params.base_url + path,
                               auth=(self.params.username,
                                     self.params.password))

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

    def test_jobs_empty(self):
        self.log.info('Testing that the server has no jobs')
        emtpy = {u'count': 0,
                 u'results': [],
                 u'previous': None,
                 u'next': None}

        r = self.get("/jobs/")
        self.assertEquals(r.json(), emtpy)

    def test_jobs_add(self):
        self.log.info('Testing that a new job can be added')
        job = {u'id': u'a0a272a09d2edda895bae4d75f5aebfad6562fb0',
               u'status': 'NOSTATUS',
               u'activities': [],
               u'tests': [],
               u'name': u'foobar job',
               u'priority': 'MEDIUM',
               u'timeout': 0}

        data = {"id": "a0a272a09d2edda895bae4d75f5aebfad6562fb0",
                "name": "foobar job",
                "priority": "MEDIUM",
                "status": "NOSTATUS"}
        r = self.post("/jobs/", data)
        self.assertEquals(r.json(), job)

    def test_jobs_del(self):
        self.log.info('Testing that a job can be deleted')
        jobs = self.get('/jobs/').json()
        job = jobs['results'][0]
        path = "/jobs/" + job['id'] + "/"
        self.log.debug('Deleting job using path: %s', path)
        r = self.delete(path)
        self.test_jobs_empty()

    def action(self):
        self.test_version()
        self.test_jobstatus_list()
        self.test_jobstatus_noadd()
        self.test_teststatus_list()
        self.test_teststatus_noadd()
        self.test_jobs_empty()
        self.test_jobs_add()
        self.test_jobs_del()
