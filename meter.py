import time

class Meter:
     def __init__(self, max_meter_setting):
          self._max_setting = max_meter_setting
          
          self._setting = 0
          self._start_time = round(time.time())
          
     @property
     def setting(self):
          return self._setting
     
     @setting.setter
     def setting(self, setting):
          self._setting = setting
          
     @property
     def max_setting(self):
          return self._max_setting
     
     def busy_wait(self, seconds):
          start_busy_wait = time.time()
          while time.time() - start_busy_wait < seconds:
               continue
          
     def elapsed_seconds(self):
          return round(time.time()) - self._start_time
          