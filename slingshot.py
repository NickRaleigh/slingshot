from argparse import ArgumentParser
import os, sys
from subprocess import call
import shutil

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
