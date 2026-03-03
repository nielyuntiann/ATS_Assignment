#
#//  start_services.py
#//  
#//
#//  Created by ytguest on 2/3/26.
#//

"""
Start mock service endpoints for testing the service monitor.
- User API on port 4000 (/health)
- Auth Service on port 5000 (/version)
"""

from flask import Flask, jsonify
import threading
import random
import time

# --- User API Service ---
user_api = Flask("user_api")

@user_api.route("/health")
def health():
    return jsonify({
        "service": "User API",
        "status": "UP",
        "version": "1.2.0",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "latency_ms": int(random.uniform(10, 100))  # mock latency
    })

# --- Auth Service ---
auth_service = Flask("auth_service")

@auth_service.route("/version")
def version():
    return jsonify({
        "service": "Auth Service",
        "status": "UP",
        "version": "3.5.1",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "latency_ms": int(random.uniform(10, 100))  # mock latency
    })

def run_user_api():
    user_api.run(host="0.0.0.0", port=4000)

def run_auth_service():
    auth_service.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    # Run both services in separate threads
    t1 = threading.Thread(target=run_user_api, daemon=True)
    t2 = threading.Thread(target=run_auth_service, daemon=True)
    
    t1.start()
    t2.start()

    print("Mock services started: User API (4000), Auth Service (5000)")
    # Keep main thread alive
    while True:
        time.sleep(1)

