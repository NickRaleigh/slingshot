from slingshot import Slingshot
from hashlistener import HashListener

class HashHandler():
    @classmethod
    def __init__(self):
        self.state = {
            'local_active_state': HashListener.check_local_active_state(),
            'local_save_state': HashListener.check_local_save_state(),
        }
        HashListener.check_remote_active_state()

    @classmethod
    def has_is_uninitialized(self):
        return None
