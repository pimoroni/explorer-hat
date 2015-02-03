import time, threading
## Basic stoppable thread wrapper
#
#  Adds Event for stopping the execution loop
#  and exiting cleanly.
class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.daemon = True         

    def start(self):
        if self.isAlive() == False:
            self.stop_event.clear()
            threading.Thread.start(self)

    def stop(self):
        if self.isAlive() == True:
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()

## Basic thread wrapper class for asyncronously running functions
#
#  Basic thread wrapper class for running functions
#  asyncronously. Return False from your function
#  to abort looping.
class AsyncWorker(StoppableThread):
    def __init__(self, todo):
        StoppableThread.__init__(self)
        self.todo = todo

    def run(self):
        while self.stop_event.is_set() == False:
            if self.todo() == False:
                self.stop_event.set()
                break



## Collection, represents a collection of pins
#
#  Allows multiple named attributes to be added
#  to produce a clean and tidy API
class ObjectCollection:

    def __init__(self, **kwargs):
        self._all = {}
        self._aliases = {}
        self._index = []
        for name in kwargs:
                self._add_single(name,kwargs[name])

    def __iter__(self):
        for pin in self._index:
            yield self._all[pin]

    def __call__(self):
        return self

    ##  Allows pibrella.collection to return a list of members
    def __repr__(self):
        return str(', '.join( self._all.keys() ))

    def __str__(self):
        return ', '.join( self._all.keys() )

    def __len__(self):
        return len(self._index)

    # Returns all items in pins collection
    # plus an example of methods which can be called on those items
    # TODO - ensure methods presented can be called against ALL members in collection
    def __dir__(self):
        return self._all.keys() + dir(self._all[self._all.keys()[0]])

    ## Returns a pin, if its found by name,
    #  otherwise tries to run the named function against all pins
    def __getattr__(self,name):
        # Return the pin if we have it
        if name in self._all.keys():
            return self._all[name]
        if name in self._aliases.keys():
            return self._aliases[name]
        # Otherwise try to run against all pins
        else:
            def handlerFunction(*args,**kwargs):
                return self._do(name,*args,**kwargs)
            handlerFunction.__name__ = name
            return handlerFunction

    ## Support accessing with [n]
    def __getitem__(self, key):
        if isinstance(key,int):
            return self._all[self._index[key]]
        else:
            return self._all[key]

    ## Runs a function against all registered pins
    #
    # Ask for a specific method to be run
    # against all added pins
    def _do(self,name,*args,**kwargs):
        _results = {}
        for node in self._index:
            handler = getattr(self._all[node],name)
            if hasattr(handler, '__call__'):
                _results[node] = handler(*args)
            else:
                _results[node] = handler
        return _results

    def count(self):
        return self.all.count()

    def _alias(self,**kwargs):
        for name in kwargs:
            self._add_alias(name,kwargs[name])

    def _add(self,**kwargs):
        for name in kwargs:
            self._add_single(name,kwargs[name])

    def _add_alias(self,name,target):
        self._aliases[name] = self._all[target]

    def _add_single(self,name,obj):
        # Handle adding additional items after init
        self._all[name] = obj
        self._index.append(name)

    def each(self, handler):
        '''Iterate through each item in the collection
        and pass them to "handler" function in turn as
        the sole argument.'''
        for name in self._all.keys():
            handler(self._all[name])
