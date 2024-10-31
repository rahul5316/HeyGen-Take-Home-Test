import requests
import time
import sys

class JobStatusChecker:
    
    def __init__(self, base_url, max_wait_time=60, max_retries=10):
        
        self.base_url = base_url
        self.max_wait_time = max_wait_time
        self.max_retries = max_retries

    def start_job(self):
        try:
            response = requests.post(f"{self.base_url}/start_job", timeout=5)
            response.raise_for_status()
            job_id = response.json().get('job_id')
            if job_id:
                return job_id
            else:
                raise Exception("No job_id returned from server.")
            
        except requests.RequestException as e:
            raise Exception(f"Error starting job: {e}")

    def resolve_job(self, job_id):
        start_time = time.time()
        attempt = 0
        wait_time = 1

        while time.time() - start_time < self.max_wait_time:
            try:
                params = {'job_id': job_id}
                response = requests.get(f"{self.base_url}/status", params=params, timeout=5)
                response.raise_for_status()
                result = response.json().get('result', 'pending')

                if result in ['completed', 'error']:
                    return result

                print(f"Job {job_id} status: {result}")

                time.sleep(wait_time)
                attempt += 1

                if attempt >= self.max_retries:
                    wait_time = min(wait_time * 2, self.max_wait_time - (time.time() - start_time))
                    attempt = 0

            except requests.RequestException as e:
                print(f"Network error occurred: {e}")
                time.sleep(wait_time)
                attempt += 1

        raise TimeoutError("Job did not complete within the maximum wait time.")


if __name__ == '__main__':
    checker = JobStatusChecker('http://127.0.0.1:5000', max_wait_time=60)

    try:
        if len(sys.argv) > 1:
            # User provided one or more job_ids
            job_ids = sys.argv[1:]
            
            for job_id in job_ids:
                print(f"Using existing job ID: {job_id}")
                status = checker.resolve_job(job_id)
                print(f"Job {job_id} status: {status}")
        else:
                # no jobID provided, we start a new job
            job_id = checker.start_job()
            print(f"Started new job with ID: {job_id}")
            status = checker.resolve_job(job_id)
            print(f"Job {job_id} status: {status}")
            
    except Exception as e:
        print(str(e))

