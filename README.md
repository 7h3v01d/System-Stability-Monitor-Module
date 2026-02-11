# System Stability Monitor Module

A lightweight, non-blocking Python module designed to monitor system resources (CPU/GPU) and provide a Peak Alert signal to throttle heavy processes during high system stress.

### Features
- Low Overhead: Uses psutil and GPUtil with optimized polling intervals.
- Hysteresis Logic: Includes a safety margin (95% trigger, 80% recovery) to prevent "flapping" between states.
- Asynchronous: Runs in a background thread so it doesn't lag your main application.
- GUI & CLI Compatible: Includes a simple live-view dashboard.

## Installation
Ensure you have the required dependencies installed in your environment:
```Bash
pip install psutil gputil
```

## Project Structure
- `monitor.py`: The core logic module. Import this into your project.<br>
- `main_gui.py:` A standalone visual dashboard to see live readings and alert status.

## Usage (Integration)To use the monitor as a throttle controller in your own program:

```Python
from monitor import monitor
import time

def my_heavy_process():
    # Check the monitor state
    stats = monitor.get_stats()
    
    if stats['peak_alert']:
        print("System Stressed! Throttling back...")
        time.sleep(1)  # Example throttle: add delay
    else:
        # Run at full speed
        pass

while True:
    my_heavy_process()
```
### Logic Configuration

You can adjust the sensitivity in monitor.py by changing these values in the SystemMonitor initialization:
| Parameter          | Default | Description                                     |
|:-------------------|:--------|:------------------------------------------------|
| `threshold`          | 95.0    | Usage % that triggers the Peak Alert.           |
| `recovery_threshold` | 80.0    | Usage must drop below this to clear the alert.  |
| `trigger_seconds`    |  2      | Duration at peak before the alert fires.        |
