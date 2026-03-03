#
#//  services.py
#//
#//
#//  Created by ytguest on 2/3/26.
#//

# https://copilot.microsoft.com/shares/GTgw79ARFs93g1FbPyfrc

"""
Scheduler that periodically enqueues service health check tasks
based on each service's interval_check. A single worker thread
consumes tasks and executes health checks.
"""

import threading
import time
import queue
from core.loader import get_services
from core.health_checker import check_service
from core.data_writer import result_queue

# Shared work queue for tasks
task_queue = queue.Queue()

class Scheduler:
    def __init__(self):
        self.services = get_services()
        # Track last run time for each service
        self.last_run = {s["name"]: 0 for s in self.services}
        
    def start(self):
        # Launch scheduler loop in background
        threading.Thread(target=self.schedule_loop, daemon=True).start()
        # Launch single worker loop in background
        threading.Thread(target=self.worker_loop, daemon=True).start()
    
    def schedule_loop(self):
        """Continuously check intervals and enqueue tasks."""
        print("Starting schedule loop.. ")
        while True:
            now = time.time()
            for service in self.services:
                last = self.last_run[service["name"]]
                interval = service["interval_check"]
                if now - last >= interval:
                    task_queue.put(service)
                    self.last_run[service["name"]] = now
            time.sleep(1)  # avoid busy loop
    
    def worker_loop(self):
        """Worker consumes tasks and executes health checks."""
        while True:
            service = task_queue.get()
            result = check_service(service)
#            print("Result: ", result)
            result_queue.put(result)  # hand off to data writer
            task_queue.task_done()



# Example usage for testing
#if __name__ == "__main__":
#    import threading
#    import time
#    from data_writer import writer_loop, OUTPUT_FILE
#    import json
#    from loader import load_config, parse_config
#    
#    #
#    print("Loading config and parsing it.. ")
#    raw_config = load_config("../services.json")
#    parse_config(raw_config)
#    services = get_services()
#    
#    
#    print("Creating scheduler")
#    # Initialize scheduler
#    scheduler = Scheduler()
#    print("Scheduler created")
#    # Start scheduler and worker threads
#    scheduler.start()
#    print("Scheduler started..")
#    
#    # Start data writer thread
#    print("Writer loop started..")
#    threading.Thread(target=writer_loop, daemon=True).start()
#    
#    print("Scheduler started. Worker and data writer are running...")
#    
#    # Periodically show contents of results.json
#    while True:
#        time.sleep(10)
#        try:
#            with open(OUTPUT_FILE, "r") as f:
#                data = json.load(f)
##            print("Current results:")
#            for entry in data[-5:]:  # show last 5 entries
#                print(entry)
#        except FileNotFoundError:
#            print("No results yet...")


