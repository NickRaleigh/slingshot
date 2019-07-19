from slingshot import Slingshot
from hashlistener import HashListener
import time

class HashHandler():
    @classmethod
    def __init__(self):
        self.state = {
            'run_loop': True,
            'local_active_state': HashListener.check_local_active_state(),
            'local_save_state': HashListener.check_local_save_state(),
            'remote_active_state': HashListener.check_remote_active_state(),
            'remote_save_state': HashListener.check_remote_save_state(),
        }

        if self.is_uninitialized():
            self.mirror_active_to_saved_state()

        self.watch_loop()

    @classmethod
    def is_uninitialized(self):
        if ( len(str(self.state['local_save_state'])) == 32 and
                str(self.state['local_save_state']) != "0" and
                len(str(self.state['remote_save_state'])) == 32 and
                str(self.state['remote_save_state']) != "0"
                ):
            return False
        else:
            return True

    @classmethod
    def mirror_active_to_saved_state(self):
        self.state['local_save_state'] = self.state['local_active_state']
        self.state['remote_save_state'] = self.state['remote_active_state']

    @classmethod
    def watch_loop(self):
        try:
            while True:
                if not self.state['run_loop']:
                    break
                else:
                    new_local_active_state = HashListener.check_local_active_state()
                    new_remote_active_state = HashListener.check_remote_active_state()
                    if ( new_local_active_state != self.state['local_active_state'] and
                            new_remote_active_state == self.state['remote_active_state']
                            ):
                        print 'local file changed'
                        Slingshot.push_files()
                        self.update_state()
                    elif ( new_remote_active_state != self.state['remote_active_state'] and
                          new_local_active_state == self.state['local_active_state']
                          ):
                        print 'remote file changed'
                        Slingshot.pull_files()
                        self.update_state()
                        time.sleep(1)
        except KeyboardInterrupt:
            self.update_state(True)
            Slingshot.stop()
            exit()

    @classmethod
    def update_state(self, quitting_app=False):
        self.state['run_loop'] = False
        self.state['local_active_state'] = HashListener.check_local_active_state()
        self.state['remote_active_state'] = HashListener.check_remote_active_state()
        self.mirror_active_to_saved_state()
        Slingshot.runtime_settings['localHash'] = self.state['local_save_state']
        Slingshot.runtime_settings['remoteHash'] = self.state['remote_save_state']
        Slingshot.write_runtime_settings_to_JSON()
        self.state['run_loop'] = True
        if not quitting_app:
            self.watch_loop()
