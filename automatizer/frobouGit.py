# -*- coding: utf-8 -*-
import base64

import git
import os
import subprocess
import json


class FrobouGit(object):
    def __init__(self):
        self.config_file = "{0}/{1}".format(os.getcwd(), '.frobouGit.json')
        self.__output = {}
        if not os.path.isfile(self.config_file):
            print("{0}Configuração base não foi encontrada{1}".format('\033[1;31m', '\033[m'))
            exit(1)

    @classmethod
    # montagem da url final
    def __url_mount(self, service, name, data):
        user = "{}".format(data['username'])
        if 'password' in data and data['password'] != None:
            try:
                pwd = base64.b64decode(data['password'])
            except:
                pwd = data['password']
            data['protocol'] = 'https'
            user = "{0}:{1}".format(data['username'], pwd)
        if 'ssh-key' in data and data['ssh-key']:
            repo = data['password']
            data['protocol'] = 'ssh'
        else:
            repo = service
        if 'protocol' in data and data['protocol'] == 'ssh':
            url = "git@{0}:{1}/{2}.git".format(repo, data['username'], name)
        else:
            url = "https://{0}@{1}/{2}/{3}.git".format(user, repo, data['username'], name)
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
            print(e)
            exit(1)

    def clone(self, components=False):
        out = {}
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
                        out.update({d: "Destino {} já existe e não é um repositório válido".format(d)})
                        continue
                # se nao existir, monta a url e clona
                url = self.switch(data[d]['remote'], d, data[d])
                if not 'destination' in data[d]:
                    data[d]['destination'] = d
                self.__clone(url, data[d]['destination'], components)
        self.__output.update({'clone': out})

    def __clone(self, url, dest, components):
        try:
            # faz a clonagem
            git.Repo.clone_from(url=url, to_path=dest)
            base = os.getcwd()
            repo = git.Repo(base + '/' + dest)
            origin = repo.remotes.origin
            # pega o restante das branches
            for o in origin.refs:
                b = str(o).split('/')[1]
                if b not in ['HEAD', 'master']:
                    print(b)
                    repo.git.checkout(str(o), b=b)
            # atualizacao do composer, npm, bower, etc
            if components:
                self.__update(dest)
            print("{0}Repositório {2} clonado com sucesso{1}".format('\033[1;32m', '\033[m', dest))
        except git.GitCommandError as e:
            print("{0}Não consegui clonar o repositorio {2}. Ele já existe?{1}".format('\033[1;31m', '\033[m', dest))
            return False
        except AttributeError as a:
            print("{0}Não consegui clonar o repositorio {2}.{1}".format('\033[1;31m', '\033[m', dest))
            return False
        return True

    def sync(self, components=False):
        out = {}
        with open(self.config_file, 'r+') as config:
            data = json.load(config)
            for d in data:
                # o nome da pasta pode ser diferente do nome do repositorio, isso ajusta esse comportamento
                fld = d
                if 'destination' in data[d]:
                    fld = data[d]['destination']
                # verifica se a pasta a ser sincronizada existe
                base = "{0}".format(os.getcwd())
                folder = "{0}/{1}".format(base, fld)
                if not os.path.exists(folder):
                    out.update({fld: "Destino {} não existe".format(fld)})
                    continue
                try:
                    # verifica se é um repositorio git
                    repo = git.Repo(folder)
                except git.exc.InvalidGitRepositoryError as e:
                    out.update({fld: "Destino {} existe mas não é um repositório válido".format(fld)})
                    continue
                # verifica se a pasta nao tem alteracao
                if repo.is_dirty():
                    out.update({fld: "Destino {} tem coisas mudadas".format(fld)})
                    continue
                if self.compara(folder):
                    continue
                # todas as verificaoes ok, pode pegar os dados (so a branch atual, por enquanto)
                repo.remote().pull()
                if not self.compara(folder):
                    out.update({fld: "Destino {} tem coisas esquisitas".format(fld)})
                    continue
                # atualizacao do composer, npm, bower, etc
                if components:
                    self.__update(d, 'update')
        self.__output.update({'sync': out})

    def compara(self, folder):
        # compara o hash da origem e destino, assim eu sei que se commit local que nao tem remoto
        g = git.cmd.Git(folder)
        # pega a branch atual local
        local_branch = g.execute(['git', 'symbolic-ref', '--short', '-q', 'HEAD'])
        # pega o hash da branch atual remota
        rem = g.execute(["git", "ls-remote"])
        for head in rem.split("\n"):
            if 'refs/heads/{}'.format(local_branch) in head:
                remote_hash = head.split("\t")[0]
        # pega o hash da branch atual local
        loc = g.execute(["git", "rev-parse", local_branch])
        # compara as duas
        return remote_hash == loc

    def __update(self, path, action='install'):
        if action != 'install':
            action = 'update'
        p = os.getcwd() + '/' + path
        os.chdir(p)
        if os.path.isfile(p + '/composer.json'):
            subprocess.call(['composer', action])
        if os.path.isfile(p + '/package.json'):
            subprocess.call(['npm', action])
        if os.path.isfile(p + '/bower.json'):
            subprocess.call(['bower', action])
        os.chdir('../')

    def getResult(self):
        return self.__output
