import subprocess
from slingshot import Slingshot

class HashListener():

    @staticmethod
    def check_local_save_state():
        result = Slingshot.runtime_settings['localHash']
        return result.strip()

    @staticmethod
    def check_local_active_state():
        result = subprocess.check_output('find ' + Slingshot.runtime_settings['localDir'] + ' ' + '-printf \"%T@ %p\n" | md5sum | cut -d " " -f 1', shell=True,stderr=subprocess.STDOUT)
        return result.strip()

    @staticmethod
    def check_remote_save_state():
        result = Slingshot.runtime_settings['remoteHash']
        return result.strip()

    @staticmethod
    def check_remote_active_state():

        user = Slingshot.runtime_settings['remoteSSHUser'] + "@" if Slingshot.key_exists(Slingshot.runtime_settings, 'remoteSSHUser') else ''
        remote_command = 'find ' + Slingshot.runtime_settings['remoteDir'] + ' -printf "%T@ %p\n" | md5sum | cut -d " " -f 1'
        cmd = ( 'ssh ' + user + Slingshot.runtime_settings['remoteSSHAddress'] + ' ' + remote_command)

        result = subprocess.check_output(cmd.split())
        return result.strip()
