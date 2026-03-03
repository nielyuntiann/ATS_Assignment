"""
Data writer: consumes results from result_queue and writes to persistent JSON file.
"""

import queue
import time
import json
import os

# Shared queue for results
result_queue = queue.Queue()

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "results.json")

def init_results_file():
    """
    Ensure results.json exists and is a valid JSON array.
    """
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w") as f:
            json.dump([], f, indent=2)
    else:
        # If file exists but is invalid, reset to empty list
        try:
            with open(OUTPUT_FILE, "r") as f:
                json.load(f)
        except json.JSONDecodeError:
            with open(OUTPUT_FILE, "w") as f:
                json.dump([], f, indent=2)

def writer_loop():
    """
    Continuously flush results from queue to JSON file.
    """
    init_results_file()
    while True:
        try:
            result = result_queue.get(timeout=5)
            save_to_json(result)
            result_queue.task_done()
        except queue.Empty:
            pass
        time.sleep(1)

def save_to_json(result: dict, filename: str = OUTPUT_FILE, MAX_ENTRIES: int = 100):
    """
    Append a result entry to a JSON file.
    Args:
        result (dict): Health check result
        filename (str): Path to JSON file
    """
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # keep last 100 to prevent file from growing forever
    data.append(result)
    if len(data) > MAX_ENTRIES:
        data = data[-MAX_ENTRIES:]
    

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
