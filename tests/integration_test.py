import sys
import os
import threading
import time
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from server.server import app 
from client.client import JobStatusChecker

def run_server():
    #starting the server
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    

def integration_test():
    
    #Integration test that starts the server and uses the client library.
    
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    logging.info("Server started separately.")

    time.sleep(1)

    checker = JobStatusChecker('http://127.0.0.1:5000', max_wait_time=60)
    
    try:
        job_id = checker.start_job()
        logging.info(f"Started job with ID: {job_id}")
        status = checker.resolve_job(job_id)
        logging.info(f"Job {job_id} status: {status}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    integration_test()
