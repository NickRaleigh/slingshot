import subprocess
from slingshot import Slingshot

class HashListener():

    @staticmethod
    def check_local_save_state():
        result = Slingshot.runtime_settings['localHash']
        return result

    @staticmethod
    def check_local_active_state():
        result = subprocess.check_output('find ' +
                                         Slingshot.runtime_settings['localDir'] + ' ' +
                                         '-printf \"%T@ %p\n" | md5sum | cut -d " " -f 1', shell=True,stderr=subprocess.STDOUT)
        return result

    @staticmethod
    def check_remote_save_state():
        result = Slingshot.runtime_settings['remoteHash']
        return result

    @staticmethod
    def check_remote_active_state():
        user = Slingshot.runtime_settings['remoteSSHUser'] + "@" if Slingshot.key_exists(Slingshot.runtime_settings, 'remoteSSHUser') else ''
        result = subprocess.check_output('ssh ' +
                                         user +
                                         Slingshot.runtime_settings['remoteSSHAddress'] + ' ' +
                                         'find ' +
                                         Slingshot.runtime_settings['remoteDir'] + ' ' +
                                         '-printf ' + 
                                         '\\"%T@ %p\\n"' + ' ' +
                                         '| md5sum | cut -d " " -f 1', shell=True,stderr=subprocess.STDOUT)
        print 'BEEP: ' + result
        return result
