# -*- coding: utf-8 -*-
import git
import os
import subprocess
import json


class FrobouGit(object):
    def __init__(self):
        self.config_file = "{0}/{1}".format(os.getcwd(), '.frobouGit.json')
        if not os.path.isfile(self.config_file):
            print("{0}Configuração base não foi encontrada{1}".format('\033[1;31m', '\033[m'))
            exit(1)
            # https://username:password@github.com/username/repository.git
            # https://github.com/frobou/frobou-db-connect.git
            # ssh://git@ispti_portal:frobou/git-automatizer.git
            # ssh://git@github.com:frobou/git-automatizer.git
            # https://efepimenta@bitbucket.org/efepimenta/ispti-portal-api.git
            # ssh://git@bitbucket.org:efepimenta/ispti-portal-api.git
            # {'remote': remote, 'protocol': protocol, 'username': username, "ssh-key": ssh_key,'password': password}
            '''
            opts = [ "https://username:password@github.com/username/repository.git",
                    "https://github.com/frobou/frobou-db-connect.git",
                    "ssh://git@ispti_portal:frobou/git-automatizer.git",
                    "ssh://git@github.com:frobou/git-automatizer.git",
                    ]

            for st in opts:
                url = st.split('/')[2]
                if '@' in url:
                    seg1,seg2 = url.split('@')
                    usuario = seg1
                if ':' in seg1:
                    usuario,senha = seg1.split(':')
                    print("usuario: {}".format(usuario))
                if senha: print("senha: {}".format(senha))
                    print("site: {}\n".format(seg2))
            '''

    @classmethod
    def __url_mount(self, service, name, data):
        user = "{}".format(data['username'])
        if 'password' in data and data['password'] != None:
            data['protocol'] = 'https'
            user = "{0}:{1}".format(data['username'], data['password'])

        if 'ssh-key' in data and data['ssh-key']:
            repo = data['password']
            data['protocol'] = 'ssh'
        else:
            repo = service
        if 'protocol' in data and data['protocol'] == 'ssh':
            url = "git@{0}:{1}/{2}.git".format(repo, data['username'], name)
        else:
            url = "https://{0}@{1}/{2}/{3}.git".format(user, repo, data['username'], name)

        print(url)
        return url

    @classmethod
    def __github(self, name, data):
        return self.__url_mount('github.com', name, data)

    @classmethod
    def __bitbucket(self, name, data):
        return self.__url_mount('bitbucket.org', name, data)

    @classmethod
    def switch(self, remote, name, data):
        switcher = {
            'github': self.__github,
            'bitbucket': self.__bitbucket
        }
        try:
            func = switcher.get(remote)
            return func(name, data)
        except TypeError as e:
            print("{0}Remote {1} não foi encontrado{2}".format('\033[1;31m', name, '\033[m'))
            exit(1)

    def clone(self):
        with open(self.config_file, 'r+') as config:
            data = json.load(config)
            for d in data:
                # verifica se o dir ja existe
                base = "{0}".format(os.getcwd())
                folder = "{0}/{1}".format(base, d)
                # se existir, verifica se é um repositório GIT
                if os.path.exists(folder):
                    try:
                        git.Repo(folder)
                    except git.exc.InvalidGitRepositoryError as e:
                        print("{0}Destino {1} já existe e não é um repositório válido{2}".format('\033[1;31m', d,
                                                                                                 '\033[m'))
                        pass
                # se nao existir, monta a url e clona
                url = self.switch(data[d]['remote'], d, data[d])
                if not 'destination' in data[d]:
                    data[d]['destination'] = d
                self.__clone(url, data[d]['destination'])

    def __clone(self, url, dest):
        try:
            git.Repo.clone_from(url=url, to_path=dest)
            base = os.getcwd()
            repo = git.Repo(base + '/' + dest)
            origin = repo.remotes.origin
            for o in origin.refs:
                b = str(o).split('/')[1]
                if b not in ['HEAD', 'master']:
                    print(b)
                    repo.git.checkout(str(o), b=b)
            self.__update(dest)
            print("{0}Repositório {2} clonado com sucesso{1}".format('\033[1;32m', '\033[m', dest))
        except git.GitCommandError as e:
            print("{0}Não consegui clonar o repositorio {2}. Ele existe? Git{1}".format('\033[1;31m', '\033[m', dest))
            return False
        except AttributeError as a:
            print("{0}Não consegui clonar o repositorio {2}. Ele existe?{1}".format('\033[1;31m', '\033[m', dest))
            return False
        return True

    def pobrema(self, path):
        ssh_cmd = 'ssh -i ~/.ssh/id_rsa git@bitbucket.org'
        with git.Repo.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
            git.Repo.clone_from(path, 'apitest')

    def __update(self, path):
        p = os.getcwd() + '/' + path
        os.chdir(p)
        if os.path.isfile(p + '/composer.json'):
            subprocess.call(['composer', 'install'])
        if os.path.isfile(p + '/package.json'):
            subprocess.call(['npm', 'install'])
        if os.path.isfile(p + '/bower.json'):
            subprocess.call(['bower', 'install'])
        os.chdir('../')

    def sync(self):
        pass
