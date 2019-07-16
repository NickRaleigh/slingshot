import time
from new import Slingshot
from handler import EventHandler
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class App:
    @classmethod
    def __init__(self):
        global Slingshot
        Slingshot = Slingshot()
        self.run()

    @classmethod
    def run(self):
        event_handler = EventHandler()
        observer = Observer()
        observer.schedule(event_handler, Slingshot.data['localDir'], recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            Slingshot.stop()
        observer.join()

# Runtime
global App
App = App()

