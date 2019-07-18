import json
import os, sys
from subprocess import call
from argparse import ArgumentParser
import shutil

class Slingshot:
    @classmethod
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument(dest="action")
        parser.add_argument(dest="name")
        self.cli_args = parser.parse_args()

        self.load_sling_JSON()
        self.lookup_name()
        self.route_action()

    @classmethod
    def lookup_name(self):
        for JSON_setting in self.sling_JSON_data:
            if JSON_setting['name'] == self.cli_args.name:
                self.runtime_settings = JSON_setting
                break

    @classmethod
    def route_action(self):
        if self.cli_args.action == "start":
            self.make_dir()
            self.pull_files()
            print("Pull Sync Complete.")

        elif self.cli_args.action == "pull":
            self.pull_files()
            print("Push Sync Complete.")
            exit()

        elif self.cli_args.action == "push":
            self.push_files()
            print("Sync Complete.")
            exit()

        elif self.cli_args.action == "new":
            self.add_new()
            exit()

    @classmethod
    def add_new(self):
        new_setting = {
            "name": self.cli_args.name,
            "targetSSHUser": "username",
            "targetSSHAddress": "10.0.0.1",
            "targetDir": "/path/on/server/",
            "localDir": "/path/to/local/",
            "isFile": "false",
            "destroyOnExit": "true"
        }
        self.sling_JSON_data.append(new_setting)
        with open('./sling.json', 'w') as f:
            json.dump(self.sling_JSON_data, f, indent=2)
        print("Added new setting for " + self.cli_args.name + '. You can sync it with your remote machine by running slingshot start ' + self.cli_args.name + '.')

    @classmethod
    def load_sling_JSON(self):
        with open('./sling.json') as f:
            self.sling_JSON_data = json.load(f)

    @classmethod
    def make_dir(self):
        if not os.path.exists(self.runtime_settings['localDir']):
            os.mkdir(self.runtime_settings['localDir'])
            print("Slingshot instance created.")

    @classmethod
    def key_exists(self, dictionary, key):
        for k, v in dictionary.items():
            if k == key:
                return True
                break
        return False

    @classmethod
    def pull_files(self):
        dirFlag = '-r ' if self.runtime_settings['isFile'] == 'false' else ''
        deleteFlag = '--delete ' if self.runtime_settings['isFile'] == 'false' else ''
        user = self.runtime_settings['targetSSHUser'] + "@" if self.key_exists(self.runtime_settings, 'targetSSHUser') else ''
        cmd = (
            'rsync ' +
            dirFlag +
            '-av ' +
            user +
            self.runtime_settings['targetSSHAddress'] + ':' +
            self.runtime_settings['targetDir'] + ' ' +
            self.runtime_settings['localDir'] + ' ' +
            '--rsh=ssh ' +
            # '--progress ' +
            '--no-motd ' +
            deleteFlag
        )
        call(cmd.split())

    @classmethod
    def push_files(self):
        dirFlag = '-r ' if self.runtime_settings['isFile'] == 'false' else ''
        user = self.runtime_settings['targetSSHUser'] + "@" if self.key_exists(self.runtime_settings, 'targetSSHUser') else ''
        deleteFlag = '--delete ' if self.runtime_settings['isFile'] == 'false' else ''
        cmd = (
            'rsync ' +
            dirFlag +
            '-av ' +
            user +
            self.runtime_settings['localDir'] + ' ' +
            self.runtime_settings['targetSSHAddress'] + ':' +
            self.runtime_settings['targetDir'] + ' ' +
            '--rsh=ssh ' +
            # '--progress ' +
            '--no-motd ' +
            deleteFlag
        )
        call(cmd.split())

    @classmethod
    def stop(self):
        if self.runtime_settings['destroyOnExit'] == 'true':
            shutil.rmtree(self.runtime_settings['localDir'])
            print("\nSlingshot instance destroyed.")


