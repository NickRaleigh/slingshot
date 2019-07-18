import os
import subprocess
import time
from slingshot import Slingshot

class RemoteListener:
    @classmethod
    def __init__(self):
        self.state = {
            'running': False,
            'md5sum': self.getmd5sum()
        }

    @classmethod
    def watch(self):
        watcherIsRunning = self.state['running']
        while watcherIsRunning:
            if watcherIsRunning:
                self.updateState()
                watcherIsRunning = self.isRunning()
                time.sleep(1)
            else:
                break

    @classmethod
    def isRunning(self):
        return False if not self.state['running'] else True

    @classmethod
    def getmd5sum(self):
        remote_command = 'find /home/nick/Development/playground/test -printf "%T@ %p\n" | md5sum | cut -d " " -f 1'
        cmd = ( 'ssh papapumplocal ' + remote_command)
        result = subprocess.check_output(cmd.split())
        return result

    @classmethod
    def updateState(self):
        new_state = self.getmd5sum()
        if new_state != self.state['md5sum']:
            Slingshot.pull_files()
            self.state['md5sum'] = new_state

    @classmethod
    def stopRunning(self):
        self.state['running'] = False
        print 'stop running'
        self.watch()

    @classmethod
    def startRunning(self):
        self.state['running'] = True
        print 'startrunning'
        self.watch()
