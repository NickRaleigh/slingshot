import subprocess
from slingshot import Slingshot

class LocalHash():

    @staticmethod
    def checkSaveState():
        result = Slingshot.runtime_settings['localHash']
        print result
        return result

    @staticmethod
    def checkActiveState():
        result = subprocess.check_output('find ' +
                                         Slingshot.runtime_settings['localDir'] + ' ' +
                                         '-printf \"%T@ %p\n" | md5sum | cut -d " " -f 1', shell=True,stderr=subprocess.STDOUT)
        print result
        return result
