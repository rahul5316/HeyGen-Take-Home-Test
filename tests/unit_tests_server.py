import unittest
import sys
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from server.server import app

class TestServer(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_start_job(self):
        response = self.client.post('/start_job')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('job_id', data)

    def test_get_status_without_job_id(self):
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'job_id parameter is required')

    def test_get_status_with_invalid_job_id(self):
        response = self.client.get('/status', query_string={'job_id': 'invalid'})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Job not found')

    def test_job_lifecycle(self):
        response = self.client.post('/start_job')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        job_id = data['job_id']

        response = self.client.get('/status', query_string={'job_id': job_id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], 'pending')

        from server.server import jobs
        jobs[job_id] = 'completed'

        response = self.client.get('/status', query_string={'job_id': job_id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], 'completed')

if __name__ == '__main__':
    unittest.main()
