import time
from slingshot import Slingshot
from RemoteListener import RemoteListener
from multiprocessing import Process
from localhash import LocalHash

class App:
    @classmethod
    def __init__(self):
        global Slingshot
        global RemoteListener
        Slingshot = Slingshot()
        # RemoteListener = RemoteListener()
        LocalHash.checkActiveState()
        LocalHash.checkSaveState()
        self.run()

    @classmethod
    def run(self):
        return None

# Runtime
App = App()

