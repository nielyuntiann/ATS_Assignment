#
//  plan.py
//  
//
//  Created by ytguest on 2/3/26.
//

1. Configuration loader
- load a configuration file describing services:
    - endpoint URL
    - availability / status
    - version (if available)

services.json
[
  {
    "name": "User API",
    "uri": "http://localhost:4000/health",
    "expected_version": "1.2.0",
    "interval_check": "60"
  },
  {
    "name": "Auth Service",
    "uri": "http://localhost:5000/version",
    "expected_version": "3.5.1"
    "interval_check": "120"
  },
  "pool": 10
]
i.e. python app.py config_file.json
starts on port 8000 by default
starts x pool of threads



2. Periodically ping each service and record its information
- interval_check:
    - spawns a scheduler continuously schedule work
- pool_of_threads:
    - round robin pick a thread, pick the next ask
- write returned data to a queue for the data writer

    
3. Data writer
every x second check queue for new data, flush to json file



4. Expose Result through Alert Mechanism, FastAPI or Flask
- SSE
- /api/health: Json api
{
  "User API": { Name
    "status": "UP",
    "latency_ms": 120,
    "version": "1.2.0",
    "last_checked": "2026-03-02T11:40:00"
  },
  "Auth Service": {
    "status": "DOWN",
    "latency_ms": null,
    "version": null,
    "last_checked": "2026-03-02T11:40:00"
  }
}
- /dashboard: webpage  dashboard
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    # Render HTML template with service data
    return render_template("dashboard.html", services=get_latest_status())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


Uptime % → ratio of UP vs DOWN checks over time.
Avg Response → mean latency across checks.
Incidents → count of DOWN events.
Healthy Services → number of services currently UP.


ATS_Take_Home_Assignment
    - api
    - core
        - data_writer.py
        - health_checker.py
        - loader.py
        - results.json
        - scheduler.py
    - services.json
    - start_mock_services.py
    - static
        - css
            - dashboard.css
        - js
            - dashboard.js
    - templates
        - dashboard.html


service-monitor/
├── app.py               # Entrypoint: loads config, starts threads, launches Flask
├── core/
│   ├── loader.py           # Load and validate configuration (services.json)
│   ├── scheduler.py        # Interval scheduling logic
│   ├── worker_pool.py      # Thread pool management (round robin)
│   ├── health_checker.py   # Ping services, measure latency, version
│   └── data_writer.py      # Flush queue to JSON
│   └── results.json      # Flush queue to JSON
├── api/
|
├── static/                 # CSS/JS for dashboard
│   └── css
│       └── dashboard.css
│   └── js
│       └── dashboard.js
├── templates/              # HTML templates (dashboard.html)
│   └── dashboard.html
└── services.json           # Example configuration file

│   ├── server.py           # Flask app setup, routes
│   ├── sse.py              # SSE implementation (/subscribe endpoint)
│   └── dashboard.py        # HTML dashboard rendering (/dashboard)

├── requirements.txt        # Python dependencies
├── Dockerfile              # Container build file
├── docker-compose.yml      # Optional orchestration
├── README.md               # Documentation & rationale


loader.py
- load_config fn
- parse_config: extracts Name, URI, Expected Version, interval of check
    and pool_size,
    set the params in global memory

scheduler.py
- read from global memory get_pool_size and launch pool_size num of threads
- a scheduler would run, continuously adding tasks based on 'interval_check' and add to a work queue
- a worker would assign thread to a task

