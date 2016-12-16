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

    def pobrema(self, path):
        ssh_cmd = 'ssh -i ~/.ssh/id_rsa git@bitbucket.org'
        with git.Repo.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
            git.Repo.clone_from(path, 'apitest')

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
