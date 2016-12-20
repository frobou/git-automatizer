# -*- coding: utf-8 -*-
import getpass

from git_automatizer.frobouConfig import FrobouConfig

g = FrobouConfig()

pwd = getpass.getpass('Password: ')
g.add_project(repo='ApiTest', remote='bitbucket', protocol='ssh', username='frobou', ssh_key=False,
              password=pwd, to_foler='ApiTest')

# g.remove_project('ApiTest')

# g.repo_list()
