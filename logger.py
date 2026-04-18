import random
import time
from threading import Thread, Lock

class LoggerThreads:
     _LOGGING_TIME = 2
     _PRINT_MARGIN = 25
     _MIN_SLEEP_TIME = 0
     _MAX_SLEEP_TIME = 1
     
     def __init__(self,meter,
                  loggers_count,
                  setting_mutex,
                  logging_semaphore,
                  setting_started_event):
          self._meter = meter
          self._loggers_count = loggers_count
          self._setting_mutex = setting_mutex
          self._logging_semaphore = logging_semaphore
          self._setting_started_event = setting_started_event
          
          self._printing_mutex = Lock()
          self._threads = []
          
          for i in range(self._loggers_count):
               self._threads.append(
                    Thread(target=self._log_meter, args=(i + 1,)))
               
     def start(self):
          for thread in self._threads:
               thread.start()
               
     def finish(self):
          for thread in self._threads:
               thread.join()
               
     def _log_meter(self, thread_id):
          self._setting_started_event.wait()
          keep_logging = True
          
          while keep_logging:
               time.sleep(
                    random.randint(LoggerThreads._MIN_SLEEP_TIME,
                                   LoggerThreads._MAX_SLEEP_TIME)
               )
               
               while self._setting_mutex.locked():
                    continue
               
               with self._logging_semaphore:
                    setting = self._meter.setting
                    time_started = self._meter.elapsed_seconds()
               
               if setting > 0:
                    with self._printing_mutex:
                         print(''*self._PRINT_MARGIN, f'{time_started:02d} LOGGER #{thread_id} logging {setting}', flush=True)
                         
                    self._meter.busy_wait(LoggerThreads._LOGGING_TIME)
               else:
                    keep_logging = False
                    with self._printing_mutex:
                         print(''*self._PRINT_MARGIN, f'{time_started:02d} LOGGER #{thread_id} logging {setting}', flush=True)
                    
                    