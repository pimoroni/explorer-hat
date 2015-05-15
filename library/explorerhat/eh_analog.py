from eh_common import AsyncWorker
import time

class AnalogInput(object):
    type = 'Analog Input'

    def __init__(self, adc, channel):
        self.channel = channel
        self._sensitivity = 0.1
        self._t_watch = None
        self.last_value = None
        self.adc = adc

    def read(self):
        return self.adc.read_se_adc(self.channel)

    def sensitivity(self, sensitivity):
        self._sensitivity = sensitivity

    def changed(self, handler, sensitivity=None):
        self._handler = handler
        if sensitivity != None:
            self._sensitivity = sensitivity
        if self._t_watch == None:
            self._t_watch = AsyncWorker(self._watch)
            self._t_watch.start()
 
    def _watch(self):
        value = self.read()
        if self.last_value != None and abs(value-self.last_value) > self._sensitivity:
            if callable(self._handler):
                self._handler(self, value)
        self.last_value = value
        time.sleep(0.01)