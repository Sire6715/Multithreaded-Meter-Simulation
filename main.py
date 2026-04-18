from threading import Lock, Semaphore, Event
from meter import Meter
from technician import TechnicianThreads
from logger import LoggerThreads

MAX_METER_SETTING = 4
TECHNICIANS_COUNT = 3
LOGGERS_COUNT = 3

def run_simulation():
     setting_mutex = Lock()
     logging_semaphore = Semaphore(LOGGERS_COUNT)
     setting_started_event = Event()
     
     meter = Meter(MAX_METER_SETTING)
     
     technician_threads = TechnicianThreads(meter,
                                             TECHNICIANS_COUNT,
                                             LOGGERS_COUNT,
                                             setting_mutex,
                                             logging_semaphore,
                                             setting_started_event)
     
     logger_threads = LoggerThreads(meter,
                                    LOGGERS_COUNT,
                                    setting_mutex,
                                    logging_semaphore,
                                    setting_started_event)
     
     technician_threads.start()
     logger_threads.start()
     
     technician_threads.finish()
     logger_threads.finish()
     
if __name__ == '__main__':
     run_simulation()
     
     print()
     print('Program done!')