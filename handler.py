from watchdog.events import FileSystemEventHandler
from slingshot import Slingshot

class EventHandler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        print "Created: " + event.src_path
        # Slingshot.push_files()

    @staticmethod
    def on_deleted(event):
        print "Deleted: " + event.src_path
        Slingshot.push_files()

    @staticmethod
    def on_modified(event):
        print "Modified: " + event.src_path
        Slingshot.push_files()

    @staticmethod
    def on_moved(event):
        print "Moved: " + event.src_path
        Slingshot.push_files()
