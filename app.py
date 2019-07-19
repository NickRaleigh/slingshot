import time
from slingshot import Slingshot
from RemoteListener import RemoteListener
from multiprocessing import Process
from hashhandler import HashHandler

class App:
    @classmethod
    def __init__(self):
        global Slingshot
        global RemoteListener
        global HashHandler
        Slingshot = Slingshot()
        HashHandler = HashHandler()
        self.run()

    @classmethod
    def run(self):
        return None

# Runtime
App = App()

