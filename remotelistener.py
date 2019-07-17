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
        while self.state['running']:
            self.updateState()
            print self.state['md5sum']
            time.sleep(1)

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
    def stopRunnning(self):
        self.state['running'] = False
        print 'stop running'

    @classmethod
    def startRunnning(self):
        self.state['running'] = True
        print 'start running'
