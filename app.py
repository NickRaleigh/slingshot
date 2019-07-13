from argparse import ArgumentParser
import time
from subprocess import call
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os, sys
import shutil

# slingshot papapump:/home/nick/Development/sites/rightcounsel-public-web/publicsites/static/imgs/bizcounsel/page/blog/small-business.svg

# slingshot papapump:$bzImgs/page/blog/small-business.svg

# capture command line arguments

class Slingshot:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument(dest="scp_host")
        parser.add_argument(dest="scp_file")
        self.settings = parser.parse_args()
        self.DIRECTORY = ''
        self.start()

    def start(self):
        self.make_dir()
        self.download_file()
        return ''

    def make_dir(self):
        if not os.path.exists("slingshot"):
            os.mkdir('slingshot')
            self.DIRECTORY = 'slingshot'
        else:
            x=1
            while True: 
                new_dir = "slingshot-" + str(x)
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                    self.DIRECTORY = new_dir
                    break
                else:
                    x=x+1
        print("Slingshot instance " + self.DIRECTORY + " created.")

    def download_file(self):
        cmd = 'scp ' + self.settings.scp_host + ':' + self.settings.scp_file + ' ' + self.DIRECTORY
        call(cmd.split())

    def push_file(self, file):
        print self.DIRECTORY
        cmd = 'scp ' + file + ' ' + self.settings.scp_host + ':' + self.settings.scp_file
        print file + " synced."
        call(cmd.split())

    def exit(self):
        shutil.rmtree(self.DIRECTORY)
        print("\nSlingshot instance destroyed.")

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print "File change detected: - %s." % event.src_path
            Slingshot.push_file(event.src_path)

class App:
    def __init__(self):
        self.observer = Observer()
        global Slingshot
        Slingshot = Slingshot()
        self.run()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, Slingshot.DIRECTORY, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            Slingshot.exit()
            self.observer.join()

global App
App = App()

