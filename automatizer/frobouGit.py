# -*- coding: utf-8 -*-
import git
import os
import subprocess


class FrobouGit(object):
    def clone(self, url, dest):
        try:
            git.Repo.clone_from(url=url, to_path=dest)
            repo = git.Repo(os.getcwd() + '/' + dest)
            origin = repo.remotes.origin
            for o in origin.refs:
                b = str(o).split('/')[1]
                if b not in ['HEAD', 'master']:
                    print(b)
                    repo.git.checkout(str(o), b=b)
        except git.GitCommandError as e:
            print(e.stderr)
            return False
        return True


    def pobrema(self):
        # ssh_cmd = 'ssh -i id_deployment_key'
        # with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
        #     repo.remotes.origin.fetch()
        repo = git.Repo(os.getcwd())
        return repo.tags

    def update(self, path):
        p = os.getcwd() + '/' + path
        os.chdir(p)
        if os.path.isfile(p + '/composer.json'):
            subprocess.call(['composer', 'install'])
        if os.path.isfile(p + '/package.json'):
            subprocess.call(['npm', 'install'])
        if os.path.isfile(p + '/bower.json'):
            subprocess.call(['bower', 'install'])

    def sync(self):
        pass
