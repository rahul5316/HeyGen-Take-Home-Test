# HeyGen Documentation

## Overview
The JobStatusChecker client library is a Python tool for interacting with the Job Management Server. It allows users to start multiple jobs, track their progress, and handle responses based on their completion status.

Note: Ensure that the port you are using (port 5000 in this example) is not occupied by any other job. If a job is running on the port, terminate it or use a different port number.


## Client Library Usage
- Step 1: Installations
Install the requests package:

  ```pip install requests```

- Step 2: Running the Client Library
  To run the client side, execute the following command:
  ```python3 client.py```
  
- Step 3: Creating Jobs
  You can create a job using this curl command:
  
  ```curl -X POST 'http://127.0.0.1:5000/start_job'```
  
  If the job is created successfully, you will see a response like:

    {
      "job_id": "1730329958865"
    }
  
- Step 4: Checking Job Status
  
The library handles multiple jobs concurrently, storing them in a dictionary on the server side.

- To check the status of a job, use the following command:

  ```python3 client.py job_id```
  
```If you run python3 client.py without a job ID, the library will create and execute a new job.```

## Server Library Usage

The client side interacts with a Flask-based server that provides endpoints for starting and monitoring asynchronous jobs. Each job has a 10% chance of failure, simulating a realistic process.

## Requirements
- Python 3 or higher
- Flask Library
- Install Flask with the following commands if not already installed:

```pip install Flask```
```pip install Flask requests```
- Running the Server
  To run the server, execute:
  ```python3 server.py```
