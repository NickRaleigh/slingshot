import time
from watchdog.events import FileSystemEventHandler
from slingshot import Slingshot
from RemoteListener import RemoteListener

class EventHandler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        print "Created: " + event.src_path
        EventHandler.push()

    @staticmethod
    def on_deleted(event):
        print "Deleted: " + event.src_path
        EventHandler.push()

    @staticmethod
    def on_modified(event):
        print "Modified: " + event.src_path
        EventHandler.push()

    @staticmethod
    def on_moved(event):
        print "Moved: " + event.src_path
        EventHandler.push()

    @staticmethod
    def push():
        RemoteListener.stopRunning()
        Slingshot.push_files()
        RemoteListener.updateState()
        time.sleep(1)
        RemoteListener.watch()

