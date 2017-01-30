# -*- coding: utf-8 -*-
import base64
import os
import json

# http://stackoverflow.com/questions/30216662/python-argparse-provide-different-arguments-based-on-parent-argument-value

class FrobouConfig(object):
    def __init__(self):
        self.config_file = "{0}/{1}".format(os.getcwd(), '.frobouGit.json')
        if not os.path.isfile(self.config_file):
            with open(self.config_file, 'w') as config:
                json.dump({}, config)

    def add_project(self, repo, service, protocol='ssh', username=None, ssh_key=False, password=None, to_foler=None):
        if repo.strip() == "":
            print("{0}repo não pode ser em branco{1}".format('\033[1;31m', '\033[m'))
            exit(1)
        if service.strip() == "":
            print("{0}service não pode ser em branco{1}".format('\033[1;31m', '\033[m'))
            exit(1)
        if to_foler == None:
            to_foler = repo
        try:
            with open(self.config_file, 'r+') as config:
                data = json.load(config)
                if ssh_key == False:
                    pwd = password
                else:
                    pwd = base64.b64encode(password.encode('utf8')).decode('utf8')
                data[repo] = {'service': service, 'protocol': protocol, 'username': username, "ssh-key": ssh_key,
                              'password': pwd,
                              "destination": to_foler}
                config.seek(0)
                json.dump(data, config, indent=2, separators=(',', ':'), ensure_ascii=False, sort_keys=False)
                config.truncate()
                print("{0}repo adicionado/alterado com sucesso{1}".format('\033[1;32m', '\033[m'))
        except TypeError as e:
            print("{0}Erro adicionando projeto porque: {1}{2}".format('\033[1;31m', e, '\033[m'))
            exit(1)

    def remove_project(self, repo):
        if repo.strip() == "":
            print("{0}repo não pode ser em branco{1}".format('\033[1;31m', '\033[m'))
            exit(1)
        try:
            with open(self.config_file, 'r+') as config:
                data = json.load(config)
                del data[repo]
                config.seek(0)
                json.dump(data, config, indent=2, separators=(',', ':'), ensure_ascii=False, sort_keys=False)
                config.truncate()
                print("{0}repo removido com sucesso{1}".format('\033[1;32m', '\033[m'))
        except Exception as e:
            print("{0}Erro removendo projeto, o nome do repositório está correto?{1}".format('\033[1;31m', '\033[m'))
            exit(1)

    def repo_list(self):
        with open(self.config_file, 'r+') as config:
            data = json.load(config)
            print("\n{0}Repositorios cadastrados:{1}".format('\033[1;37m', '\033[m'))
            for d in data:
                print("{0}{1}{2}".format('\033[1;33m', d, '\033[m'))
