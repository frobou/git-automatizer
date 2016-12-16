import os
import json


class frobouConfig(object):
    def __init__(self):
        self.config_file = "{0}/{1}".format(os.getcwd(), '.frobouGit.json')
        if not os.path.isfile(self.config_file):
            with open(self.config_file, 'w') as config:
                json.dump({}, config)

    def init(self):
        pass

    def add_project(self, repo, type, protocol, service, username, password):
        try:
            with open(self.config_file, 'r+') as config:
                data = json.load(config)
                data[repo] = {'type': type, 'protocol': protocol, 'service': service, 'username': username,
                              'password': password}
                config.seek(0)
                json.dump(data, config, indent=2, separators=(',', ':'), ensure_ascii=False)
                config.truncate()
        except Exception as e:
            print('não consegui gravar')

    def remove_project(self, repo):
        try:
            with open(self.config_file, 'r+') as config:
                data = json.load(config)
                del data[repo]
                config.seek(0)
                json.dump(data, config, indent=2, separators=(',', ':'), ensure_ascii=False)
                config.truncate()
        except Exception as e:
            print('não consegui remover')
