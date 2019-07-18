import time
from slingshot import Slingshot
from handler import EventHandler
from RemoteListener import RemoteListener
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from multiprocessing import Process

class App:
    @classmethod
    def __init__(self):
        global Slingshot
        global RemoteListener
        Slingshot = Slingshot()
        RemoteListener = RemoteListener()
        self.run()

    @classmethod
    def run(self):
        p1 = Process(target=RemoteListener.startRunning)
        p2 = Process(target=self.run_observer)

        p1.start()
        p2.start()
        p1.join()
        p2.join()

    @classmethod
    def run_observer(self):
        event_handler = EventHandler()
        observer = Observer()
        observer.schedule(event_handler, Slingshot.runtime_settings['localDir'], recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            RemoteListener.stopRunning()
            observer.stop()
            Slingshot.stop()
        observer.join()

# Runtime
App = App()

