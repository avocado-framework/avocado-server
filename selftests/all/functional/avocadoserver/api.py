"""
This functional test assumes that a previously setup server is running. In the
future this will provision the server, and shut it down after the test has been
run.

For now, only run it if you have properly setup the server as defined on
`BASE_URL`, `USERNAME` and `PASSWORD`.
"""

from avocado import test

import requests


class api(test.Test):

    BASE_URL = 'http://127.0.0.1:9405'
    USERNAME = 'admin'
    PASSWORD = '123'

    def get(self, path):
        return requests.get(self.BASE_URL + path,
                            auth=(self.USERNAME,
                                  self.PASSWORD))

    def post(self, path, data):
        return requests.post(self.BASE_URL + path,
                             auth=(self.USERNAME,
                                   self.PASSWORD),
                             data=data)

    def delete(self, path):
        return requests.delete(self.BASE_URL + path,
                               auth=(self.USERNAME,
                                     self.PASSWORD))

    def test_version(self):
        self.log.info('Testing that the server returns its version')
        r = self.get("/version/")
        self.assertEquals(r.status_code, 200)

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
               u'status': None,
               u'activities': [],
               u'tests': [],
               u'name': u'foobar job',
               u'priority': None,
               u'timeout': 0}

        data = {"id": "a0a272a09d2edda895bae4d75f5aebfad6562fb0",
                "name": "foobar job"}
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
        self.test_jobs_empty()
        self.test_jobs_add()
        self.test_jobs_del()
