class TouchSettings(object):
    type = 'Cap Touch Settings'

    def __init__(self, cap):
        self.cap = cap

    def enable_multitouch(self, en=True):
        self.cap.enable_multitouch(en)

class TouchInput(object):
    type = 'Cap Touch Input'
    
    def __init__(self, cap1208, channel, alias):
        self.alias = alias
        self._pressed = False
        self._held = False
        self.channel = channel
        self.cap1208 = cap1208
        self.handlers = {'press':None, 'release':None, 'held':None}
        for event in ['press','release','held']:
            self.cap1208.on(channel = self.channel, event=event, handler=self._handle_state)

    def _handle_state(self, channel,event):
        if channel == self.channel:
            if event == 'press':
                self._pressed = True
            elif event == 'held':
                self._held = True
            elif event in ['release','none']:
                self._pressed = False
                self._held = False
            if callable(self.handlers[event]):
                self.handlers[event](self.alias, event)

    def is_pressed(self):
        return self._pressed

    def is_held(self):
        return self._held

    def pressed(self, handler):
        self.handlers['press'] = handler

    def released(self, handler):
        self.handlers['release'] = handler

    def held(self, handler):
        self.handlers['held'] = handler