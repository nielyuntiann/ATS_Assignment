# ATS Take Home Assignment

This is the solution for the lightweight Service Reliability app that periodically checks multiple service endpoints, detects availability or version issues, and displays the latest health information in a simple, clear way.


## Quickstart

Start these seperately
```python

python3 start_mock_services.py # this will start 2 mock services

python3 app.py # this will start the service reliability monitor

```


## Start, using Docker Compose

in app.py, line 35, uncomment:
```python
# uncomment this when starting via docker-compose
# this changes the localhost uri for the mock services
# raw_config = load_config("services-docker.json")
```
then run:
```python 
docker compose up --build -d.
```




## Dashboard

To view the collected data in a dashboard, visit 
## http://127.0.0.1:8000/dashboard

# Design Overview and Tradeoffs
## 1. Event queues
The app uses event queues for writing data to an persistent json file, and for scheduling health check tasks / retrieving tasks from the task queue.

This allows different modules to run asynchronously. 
## 2. Threaded / Concurrent 
Threads are a simple way to build this app, and are great for I/O‑bound workloads.

Threaded modules: 
- Writing data runs on 1 thread (core/data_writer.py)
- Creating Health Check every x interval runs on 1 thread (core/health_checker.py)
- Reading tasks from task queue runs on 1 thread (core/scheduler.py)

This allows context switching to reduce wasted CPU cycles, since a thread on python could wait for OS to respond allowing other threads to execute in the mean time.

## 3. Monitor dashboard is synchronised through the json file
Historic logs are not required so Database is an overkill.
A json file writer that keeps the last x / 100 record is lightweight and highly responsive.





## License

[MIT](https://choosealicense.com/licenses/mit/)
