# -*- coding: utf-8 -*-
import base64

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

    @classmethod
    # montagem da url final
    def __url_mount(self, service, name, data):
        user = "{}".format(data['username'])
        if 'password' in data and data['password'] != None:
            try:
                pwd = base64.b64decode(data['password']).decode('utf-8')
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
    def switch(self, service, name, data):
        switcher = {
            'github': self.__github,
            'bitbucket': self.__bitbucket
        }
        try:
            func = switcher.get(service)
            return func(name, data)
        except TypeError:
            print(
                "{0}Serviço remoto {1} para o repositório {2} não foi encontrado{3}".format('\033[1;31m', service, name,
                                                                                           '\033[m'))
            exit(1)

    def clone(self, components=False):
        out = []
        with open(self.config_file, 'r+') as config:
            data = json.load(config)
            for d in data:
                print("{0}Iniciando a clonagem do repositório {1}{2}".format('\033[1;35m', d, '\033[m'))
                # verifica se o dir ja existe
                base = "{0}".format(os.getcwd())
                folder = "{0}/{1}".format(base, d)
                # se existir, verifica se é um repositório GIT
                if os.path.exists(folder):
                    try:
                        git.Repo(folder)
                    except git.exc.InvalidGitRepositoryError:
                        out.append({'error': {d: "Destino {} já existe e não é um repositório válido".format(d)}})
                        continue
                # se nao existir, monta a url e clona
                url = self.switch(data[d]['service'], d, data[d])
                if not 'destination' in data[d]:
                    data[d]['destination'] = d
                dt = self.__clone(url, data[d]['destination'], components)
                out += dt
        self.__print_result(out)

    def __clone(self, url, dest, components):
        out = []
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
            # tudo ok, coloca no relatório
            out.append({'success': {dest: "Repositório {} clonado com sucesso".format(dest)}})
        except git.GitCommandError:
            out.append({'error': {dest: "Repositorio {} já existe ou as credenciais estão incorretas".format(dest)}})
        except AttributeError:
            out.append({'error': {dest: "Não consegui clonar o repositorio {}".format(dest)}})
        return out

    def sync(self, components=False):
        out = []
        with open(self.config_file, 'r+') as config:
            data = json.load(config)
            for d in data:
                print("{0}Iniciando a sincronia do repositório {1}{2}".format('\033[1;34m', d, '\033[m'))
                # o nome da pasta pode ser diferente do nome do repositorio, isso ajusta esse comportamento
                fld = d
                if 'destination' in data[d]:
                    fld = data[d]['destination']
                # verifica se a pasta a ser sincronizada existe
                base = "{0}".format(os.getcwd())
                folder = "{0}/{1}".format(base, fld)
                if not os.path.exists(folder):
                    out.append({"error": {fld: "Destino {} não existe".format(fld)}})
                    continue
                try:
                    # verifica se é um repositorio git
                    repo = git.Repo(folder)
                except git.GitCommandError:
                    out.append({'error': {fld: "Provável credencial incorreta para {}".format(fld)}})
                    continue
                except git.exc.InvalidGitRepositoryError:
                    out.append({"error": {fld: "Destino {} existe mas não é um repositório válido".format(fld)}})
                    continue
                # verifica se a pasta nao tem alteracao
                if repo.is_dirty():
                    out.append({"error": {fld: "Repositório {} tem alterações pendentes".format(fld)}})
                    continue
                if self.compara(folder):
                    out.append({'ok': {"Repositório {} já está sincronizado".format(fld)}})
                    continue
                # todas as verificaoes ok, pode pegar os dados (so a branch atual, por enquanto)
                repo.remote().pull()
                if not self.compara(folder):
                    out.append({"error": {fld: "Última hash do repositório {} local é diferente da hash remota".format(fld)}})
                    continue
                # atualizacao do composer, npm, bower, etc
                if components:
                    self.__update(d, 'update')
                out.append({'success': {"Repositório {} sincronizado com sucesso".format(fld)}})
        self.__print_result(out)

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
                break
        # pega o hash da branch atual local
        loc = g.execute(["git", "rev-parse", local_branch])
        # compara as duas
        return remote_hash == loc

    def __update(self, path, action='install'):
        acao = 'instalação'
        if action != 'install':
            acao = 'atualização'
            action = 'update'
        print("{0}Fazendo a {1} dos componentes de {2}{3}".format('\033[1;33m', acao, path, '\033[m'))
        p = os.getcwd() + '/' + path
        os.chdir(p)
        if os.path.isfile(p + '/composer.json'):
            subprocess.call(['composer', action])
        if os.path.isfile(p + '/package.json'):
            subprocess.call(['npm', action])
        if os.path.isfile(p + '/bower.json'):
            subprocess.call(['bower', action])
        os.chdir('../')

    def __print_result(self, res):
        print("\n{0}Relatório final:{1}".format('\033[1;37m', '\033[m'))
        for r in res:
            if 'success' in dict.keys(r):
                for success in r['success']:
                    print("{0}{1}{2}".format('\033[1;32m', r['success'][success], '\033[m'))
            elif 'error' in dict.keys(r):
                for error in r['error']:
                    print("{0}{1}{2}".format('\033[1;31m', r['error'][error], '\033[m'))
            elif 'ok' in dict.keys(r):
                for ok in r['ok']:
                    print("{0}{1}{2}".format('\033[1;33m', ok, '\033[m'))
