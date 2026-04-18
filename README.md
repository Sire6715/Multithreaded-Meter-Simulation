#  Multithreaded Meter Simulation

A Python simulation that models concurrent **technicians** and **loggers** operating on a shared meter, demonstrating core multithreading and synchronization concepts including mutexes, semaphores, and events.

---

##  Overview

This program simulates a real-world scenario where multiple technicians periodically adjust a physical meter dial while multiple loggers concurrently observe and record the meter's readings. The challenge — and the point — is ensuring neither group interferes with the other while operating simultaneously.

---

##  How It Works

### Technicians
- Each technician runs on its own thread and makes **3 adjustment turns**
- Between turns, it sleeps for a random interval (6–10 seconds) simulating time between maintenance visits
- Before adjusting the meter, it waits until **all loggers are idle** to avoid writing while a read is in progress
- It adjusts the dial incrementally, printing each step to the terminal in real time
- Once all turns are complete, a final shutdown signal (setting of `0`) is sent to stop the loggers

### Loggers
- Each logger runs on its own thread and continuously polls the meter
- It waits for the **first technician adjustment** before it begins logging
- Before each read, it waits until no technician is actively holding the meter
- It acquires a semaphore slot to signal it is mid-read, then records the current setting and timestamp
- When it sees a setting of `0`, it logs a final entry and shuts down cleanly

---

##  Synchronization Primitives

| Primitive | Type | Purpose |
|---|---|---|
| `setting_mutex` | `Lock` | Ensures only one entity accesses the meter setting at a time |
| `logging_semaphore` | `Semaphore(3)` | Tracks how many loggers are actively reading; technician waits for full count before writing |
| `setting_started_event` | `Event` | One-time signal that fires after the first meter adjustment, unblocking all waiting loggers |
| `_printing_mutex` | `Lock` | Prevents logger threads from printing over each other on stdout |

---

##  Project Structure

```
.
├── main.py          # Entry point; wires up threads and synchronization primitives
├── meter.py         # Shared resource — the meter dial with busy_wait and timestamp utilities
├── technician.py    # Technician thread logic — adjusts the meter on a schedule
└── logger.py        # Logger thread logic — reads and records the meter setting
```

---

##  Sample Output

```
03 TECH #2:  1  2  3
                         05 LOGGER #1 logging 3
                         06 LOGGER #3 logging 3
                         06 LOGGER #2 logging 3
09 TECH #1:  1  2
                         11 LOGGER #2 logging 2
                         12 LOGGER #1 logging 2
...
23 TECH #2: done!
24 TECH #1: done!
25 TECH #3: done!
                         28 LOGGER #1 logging 0
                         28 LOGGER #2 logging 0
                         28 LOGGER #3 logging 0

Program done!
```

Technician output is left-aligned. Logger output is indented for visual separation.

---

##  Getting Started

**Requirements:** Python 3.x — no external dependencies.

```bash
# Clone the repository
git clone [https://github.com/Sire6715/<repo-name>.git](https://github.com/Sire6715/Multithreaded-Meter-Simulation.git)
cd Multithreaded-Meter-Simulation

# Run the simulation
python main.py
```

---

##  Concepts Demonstrated

- **Mutual exclusion** with `Lock` to protect shared state
- **Semaphores** to coordinate bounded concurrent access
- **Events** for one-time cross-thread signalling
- **Busy waiting** to simulate real mechanical work duration
- **Thread lifecycle management** with `start()` and `join()`
- **Race condition prevention** between concurrent readers and writers

---

##  Configuration

All simulation parameters are defined as constants and can be adjusted:

```python
# main.py
MAX_METER_SETTING = 4
TECHNICIANS_COUNT = 3
LOGGERS_COUNT     = 3

# technician.py
_TURNS           = 3
_SETTING_TIME    = 1   # seconds per dial increment
_MIN_SLEEP_TIME  = 6   # seconds between turns
_MAX_SLEEP_TIME  = 10

# logger.py
_LOGGING_TIME    = 2   # seconds to simulate recording a reading
_PRINT_MARGIN    = 25  # terminal indent for logger output
```
