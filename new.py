import json
import os, sys
from subprocess import call
import shutil

class Slingshot:
    @classmethod
    def __init__(self):
        self.load_settings()
        self.make_dir()
        self.download_file()

    @classmethod
    def load_settings(self):
        with open('./sling.json') as f:
            self.data = json.load(f)

    @classmethod
    def make_dir(self):
        if not os.path.exists(self.data['localDir']):
            os.mkdir(self.data['localDir'])
            print("Slingshot instance created.")

    @classmethod
    def download_file(self):
        dirFlag = '-r ' if self.data['isFile'] == 'false' else ''
        deleteFlag = '--delete ' if self.data['isFile'] == 'false' else ''
        cmd = (
            'rsync ' +
            dirFlag +
            self.data['targetSSHAddress'] + ':' +
            self.data['targetDir'] + ' ' +
            self.data['localDir'] + ' ' +
            deleteFlag
        )
        call(cmd.split())

    @classmethod
    def push_file(self):
        dirFlag = '-r ' if self.data['isFile'] == 'false' else ''
        deleteFlag = '--delete ' if self.data['isFile'] == 'false' else ''
        cmd = (
            'rsync ' +
            dirFlag + self.data['localDir'] + ' ' +
            self.data['targetSSHAddress'] + ':' +
            self.data['targetDir'] + ' ' +
            deleteFlag
        )
        call(cmd.split())

    @classmethod
    def stop(self):
        if self.data['destroyOnExit'] == 'true':
            shutil.rmtree(self.data['localDir'])
            print("\nSlingshot instance destroyed.")


