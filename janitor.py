# janitor.py
# StatelessStates MVP – System Hygiene Watchdog ("The Janitor")

import os
import time
import psutil   # requires 'pip install psutil'
import logging

logging.basicConfig(
    filename="janitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def monitor_processes():
    """Monitor for suspicious processes and log CPU spikes."""
    for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent"]):
        if proc.info["cpu_percent"] > 80:
            logging.warning(f"High CPU usage: {proc.info}")

def clean_temp():
    """Sanitise temporary files (simulation)."""
    temp_dir = "/tmp"
    for f in os.listdir(temp_dir):
        if f.endswith(".tmp"):
            try:
                os.remove(os.path.join(temp_dir, f))
                logging.info(f"Deleted temp file: {f}")
            except Exception as e:
                logging.error(f"Failed to delete {f}: {e}")

if __name__ == "__main__":
    logging.info("Janitor started. Monitoring system hygiene...")
    while True:
        monitor_processes()
        clean_temp()
        time.sleep(10)
