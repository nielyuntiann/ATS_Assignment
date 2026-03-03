

from flask import Flask, render_template, send_from_directory
import threading
import time
import json
import os

# Import core modules
from core.loader import load_config, parse_config, get_services
from core.scheduler import Scheduler
from core.data_writer import writer_loop, OUTPUT_FILE

# Initialize Flask
app = Flask(__name__)

# --- Flask Routes ---

@app.route("/dashboard")
def dashboard():
    # Render dashboard template
    return render_template("dashboard.html")

@app.route("/results.json")
def results():
    core_dir = os.path.join(app.root_path, "core")
    return send_from_directory(core_dir, "results.json")

# --- Entrypoint ---
if __name__ == "__main__":
    print("Loading config and parsing it...")
    raw_config = load_config("services.json")
    # uncomment this when starting via docker-compose
    # this changes the localhost uri for the mock services
    # raw_config = load_config("services-docker.json")
    
    
    parse_config(raw_config)
    services = get_services()
    print(f"Loaded {len(services)} services.")
    
    print("Creating scheduler...")
    scheduler = Scheduler()
    print("Scheduler created.")
    
    # Start scheduler and worker threads
    scheduler.start()
    print("Scheduler started.")

    # Start data writer thread
    threading.Thread(target=writer_loop, daemon=True).start()
    print("Writer loop started.")
    
    # Run Flask server
    app.run(host="0.0.0.0", port=8000)
