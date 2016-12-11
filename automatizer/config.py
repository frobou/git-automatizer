import os
import json


class frobouConfig(object):
    def __init__(self):
        self.config_file = "{0}/{1}".format(os.getcwd(), '.config.json')

    def init(self):
        pass

    def add_project(self, repo, type, protocol, service, username, password):
        try:
            with open(self.config_file, 'w') as config:
                data = {}
                data[repo] = {'type': type, 'protocol': protocol, 'service': service, 'username': username,
                              'password': password}
                json.dump(data, config, indent=2, separators=(',', ':'))
        except FileNotFoundError as e:
            print('no file config of file')

    def remove_project(self):
        pass
