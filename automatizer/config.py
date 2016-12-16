# -*- coding: utf-8 -*-
import os
import json


class frobouConfig(object):
    def __init__(self):
        self.config_file = "{0}/{1}".format(os.getcwd(), '.frobouGit.json')
        if not os.path.isfile(self.config_file):
            with open(self.config_file, 'w') as config:
                json.dump({}, config)

    def add_project(self, repo, remote, protocol='ssh', username=None, ssh_key=False, password=None, to_foler=None):
        try:
            with open(self.config_file, 'r+') as config:
                data = json.load(config)
                data[repo] = {'remote': remote, 'protocol': protocol, 'username': username, "ssh-key": ssh_key,
                              'password': password, "destination": to_foler}
                config.seek(0)
                json.dump(data, config, indent=2, separators=(',', ':'), ensure_ascii=False, sort_keys=False)
                config.truncate()
        except Exception as e:
            print('Erro adicionando projeto porque {}'.format(e.message))
            exit(1)

    def remove_project(self, repo):
        try:
            with open(self.config_file, 'r+') as config:
                data = json.load(config)
                del data[repo]
                config.seek(0)
                json.dump(data, config, indent=2, separators=(',', ':'), ensure_ascii=False, sort_keys=False)
                config.truncate()
        except Exception as e:
            print('Erro removendo projeto, o nome do repositório está correto?')
            exit(1)
