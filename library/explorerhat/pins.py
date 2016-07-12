import threading


class StoppableThread(threading.Thread):
    """Basic Stoppable Thread Wrapper

    Adds event for stopping the execution
    loop and exiting cleanly."""
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.daemon = True

    def start(self):
        if not self.isAlive():
            self.stop_event.clear()
            threading.Thread.start(self)

    def stop(self):
        if self.isAlive():
            self.stop_event.set()
            self.join()


class AsyncWorker(StoppableThread):
    """Basic thread wrapper class for asynchronously running functions

    Return False from the worker function to abort loop."""
    def __init__(self, todo):
        StoppableThread.__init__(self)
        self.todo = todo

    def run(self):
        while not self.stop_event.is_set():
            # Explicitly check for False being returned
            # from worker, IE: Don't allow None
            if self.todo() is False:
                self.stop_event.set()
                break


class ObjectCollection:
    """Represents a collection of similar objects

    Allows multiple named attributes to be
    added to produce a tidy API. Methods can then
    be called against one or all of the collections members.
    """

    def __init__(self, **kwargs):
        self._all = {}
        self._aliases = {}
        self._index = []
        for name in kwargs:
                self._add_single(name, kwargs[name])

    def __iter__(self):
        for pin in self._index:
            yield self._all[pin]

    def __call__(self):
        return self

    def __repr__(self):
        """Allows collection to return a list of members"""
        return str(', '.join(self._all.keys()))

    def __str__(self):
        return ', '.join(self._all.keys())

    def __len__(self):
        return len(self._index)

    def __dir__(self):
        """Returns all items in the collection"""
        return self._all.keys() + dir(self._all[self._all.keys()[0]])

    def __getattr__(self, name):
        """Returns a pin if found by name

        Otherwise runs named function against all pins"""

        # Return the pin if we have it
        if name in self._all.keys():
            return self._all[name]
        if name in self._aliases.keys():
            return self._aliases[name]

        # Otherwise try to run against all pins
        else:
            def handler(*args, **kwargs):
                return self._do(name, *args, **kwargs)
            handler.__name__ = name
            return handler

    def __getitem__(self, key):
        """Supprot accessing with [n]"""
        if isinstance(key, int):
            return self._all[self._index[key]]
        else:
            return self._all[key]

    def _do(self, name, *args, **kwargs):
        """Runs a function against all registered pins

        Ask for a specific method to be run against all added pins"""
        _results = {}
        for node in self._index:
            handler = getattr(self._all[node], name)
            if hasattr(handler, '__call__'):
                _results[node] = handler(*args, **kwargs)
            else:
                _results[node] = handler
        return _results

    def count(self):
        return self.all.count()

    def _alias(self, **kwargs):
        for name in kwargs:
            self._add_alias(name, kwargs[name])

    def _add(self, **kwargs):
        for name in kwargs:
            self._add_single(name, kwargs[name])

    def _add_alias(self, name, target):
        self._aliases[name] = self._all[target]

    def _add_single(self, name, obj):
        """Add a single item to the collection"""
        self._all[name] = obj
        self._all[name].name = name
        self._index.append(name)

    def each(self, handler):
        """Iterate through each item in the collection
        and pass them to "handler" function in turn as
        the sole argument."""
        for name in self._all.keys():
            handler(self._all[name])
