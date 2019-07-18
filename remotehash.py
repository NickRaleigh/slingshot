import subprocess
from slingshot import Slingshot

class RemoteHash():

    @staticmethod
    def checkSaveState():
        result = Slingshot.runtime_settings['remoteHash']
        print result
        return result

    @staticmethod
    def checkActiveState():
        user = self.runtime_settings['targetSSHUser'] + "@" if self.key_exists(self.runtime_settings, 'targetSSHUser') else ''

        cmd = ( 'ssh ' +
               user +
               self.runtime_settings['targetSSHAddress'] + ':' +
               'find ' +
               Slingshot.runtime_settings['remoteDir'] + ' ' +
               '-printf \"%T@ %p\n" | md5sum | cut -d " " -f 1'
               )
        result = subprocess.check_output(cmd, shell=True,stderr=subprocess.STDOUT)
        print result
        return result
