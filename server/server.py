from flask import Flask, jsonify, request
import threading
import time
import random

app = Flask(__name__)


PROCESSING_TIME = 20  

# 10% chance to return 'error'
ERROR_PROBABILITY = 0.1  

jobs = {}

def process_job(job_id):
    
    time.sleep(PROCESSING_TIME)
    if random.random() < ERROR_PROBABILITY:
        jobs[job_id] = 'error'
    else:
        jobs[job_id] = 'completed'

@app.route('/start_job', methods=['POST'])

def start_job():
    
    job_id = str(int(time.time() * 1000))
    jobs[job_id] = 'pending'
    threading.Thread(target=process_job, args=(job_id,), daemon=True).start()
    return jsonify({'job_id': job_id}), 200

@app.route('/status', methods=['GET'])
def get_status():
    
    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({'error': 'job_id parameter is required'}), 400
    status = jobs.get(job_id)
    if status:
        return jsonify({'job_id': job_id, 'result': status}), 200
    else:
        return jsonify({'error': 'Job not found'}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

