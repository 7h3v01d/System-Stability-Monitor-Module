
# Usage: main program, "throttle" logic would look like this:

#---------------------------------------------------------------------------- 
 
# from monitor import monitor

# def run_main_app():
    # while True:
        # data = monitor.get_stats()
        
        # if data["peak_alert"]:
            # Drop into "Low Power Mode"
            # run_lightweight_tasks()
        # else:
            # Full speed ahead
            # run_heavy_tasks()

#-----------------------------------------------------------------------------

# monitor.py

import psutil
import GPUtil
import threading
import time

class SystemMonitor:
    def __init__(self, threshold=95.0, recovery_threshold=80.0, trigger_seconds=2):
        self.stats = {"cpu": 0, "gpu": 0, "peak_alert": False}
        self.threshold = threshold
        self.recovery_threshold = recovery_threshold
        self.trigger_seconds = trigger_seconds
        self.peak_time_start = None 
        self.running = True
        
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def _update_loop(self):
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=0.5)
                gpus = GPUtil.getGPUs()
                gpu = gpus[0].load * 100 if gpus else 0

                # Check for Peak Trigger
                if cpu >= self.threshold or gpu >= self.threshold:
                    if self.peak_time_start is None:
                        self.peak_time_start = time.time()
                    if (time.time() - self.peak_time_start) >= self.trigger_seconds:
                        self.stats["peak_alert"] = True
                
                # Check for Recovery (only if we are currently in a peak_alert)
                elif self.stats["peak_alert"]:
                    if cpu < self.recovery_threshold and gpu < self.recovery_threshold:
                        self.stats["peak_alert"] = False
                        self.peak_time_start = None
                
                else:
                    # System is below threshold and not currently alerted
                    self.peak_time_start = None

                self.stats["cpu"] = cpu
                self.stats["gpu"] = gpu
            except Exception:
                pass
            
            time.sleep(0.1)

    def get_stats(self):
        return self.stats

monitor = SystemMonitor()