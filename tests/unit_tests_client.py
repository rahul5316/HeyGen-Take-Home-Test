import unittest
import sys
import os
from unittest.mock import patch
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from client.client import JobStatusChecker

class TestJobStatusChecker(unittest.TestCase):

    def setUp(self):
        self.checker = JobStatusChecker('http://127.0.0.1:5000', max_wait_time=10, max_retries=2)

    @patch('client.client.requests.post')
    def test_start_job_success(self, example_post_request):
        example_post_request.return_value.status_code = 200
        example_post_request.return_value.json.return_value = {'job_id': '12345'}
        
        job_id = self.checker.start_job()
        self.assertEqual(job_id, '12345')

    @patch('client.client.requests.post')
    def test_start_job_failure(self, example_post_request):
        example_post_request.side_effect = requests.exceptions.ConnectionError("Server not available")
        
        with self.assertRaises(Exception) as context:
            self.checker.start_job()
        self.assertIn('Error starting job', str(context.exception))

    @patch('client.client.requests.get')
    def test_resolve_job_completed(self, mock_get):
      
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'result': 'completed'}

        status = self.checker.resolve_job('12345')
        self.assertEqual(status, 'completed')
        

    @patch('client.client.requests.get')
    def test_resolve_job_pending_then_completed(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = [
            {'result': 'pending'},
            {'result': 'pending'},
            {'result': 'completed'}
        ]

        status = self.checker.resolve_job('12345')
        self.assertEqual(status, 'completed')
        

    @patch('client.client.requests.get')
    def test_resolve_job_timeout(self, mock_get):
        # Mock responses always returning pending
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'result': 'pending'}

        with self.assertRaises(TimeoutError) as context:
            self.checker.resolve_job('12345')
        self.assertIn('Job did not complete within the maximum wait time', str(context.exception))
        

    @patch('client.client.requests.get')
    def test_resolve_job_error(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'result': 'error'}

        status = self.checker.resolve_job('12345')
        self.assertEqual(status, 'error')

if __name__ == '__main__':
    unittest.main()
