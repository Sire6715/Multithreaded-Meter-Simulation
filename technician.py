import random
import time
from threading import Thread

class TechnicianThreads():
     _TURNS = 3
     _SETTING_TIME = 1
     _MIN_SLEEP_TIME = 6
     _MAX_SLEEP_TIME = 10
     
     def __init__(self, meter,
                    technicians_count,
                    loggers_count,
                    setting_mutex,
                    logging_semaphore,
                    setting_started_event):
          self._meter = meter
          self._technicians_count = technicians_count
          self._loggers_count = loggers_count
          self._setting_mutex = setting_mutex
          self._logging_semaphore = logging_semaphore
          self._setting_started_event = setting_started_event
          
          
          self._threads = []
          
          for i in range(self._technicians_count):
               self._threads.append(
                    Thread(target=self._set_meter,
                           args=(i + 1,))
               )
               
     def start(self):
          for thread in self._threads:
               thread.start()
               
     def finish(self):
          for thread in self._threads:
               thread.join()
               
          time.sleep(3)
          self._set(0, 0, 0)
          
     def _set_meter(self, thread_id):
          for turn in range(self._TURNS):
               time.sleep(
                    random.randint(self._MIN_SLEEP_TIME,
                                   self._MAX_SLEEP_TIME)
               )
               
               new_setting = random.randint(1, self._meter.max_setting)
               self._set(thread_id, turn, new_setting)
               3
      
     def _set(self, thread_id, turn, new_setting):
          with self._setting_mutex:
               while (self._logging_semaphore._value != self._loggers_count):
                    continue
               
               if new_setting > 0:
                    time_started = self._meter.elapsed_seconds()
                    print(f'{time_started:02d} TECH #{thread_id}:', end='', flush=True)
                     
                    for s in range(1, new_setting + 1):
                          self._meter.busy_wait(
                               TechnicianThreads._SETTING_TIME)
                          print(f'{s:2d}', end='', flush=True)
                    
               print(flush=True)
               
               self._meter.setting = new_setting
               self._setting_started_event.set()
               
               if turn == TechnicianThreads._TURNS - 1:
                    time_started = self._meter.elapsed_seconds()
                    print(f'{time_started:02d} TECH #{thread_id}: done!', flush=True)
                    
                    