import threading


class StoppableThread(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.func = func
        self.result = None

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        if not self.stopped():
            self.result = self.func()