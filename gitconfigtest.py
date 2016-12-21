# -*- coding: utf-8 -*-
import getpass

from git_automatizer.frobouConfig import FrobouConfig

g = FrobouConfig()

pwd = getpass.getpass('Password: ')
g.add_project(repo='repo_name', service='github', protocol='ssh', username='username', ssh_key=False,
              password=pwd, to_foler='repo_folder')

# g.remove_project('ApiTest')

# g.repo_list()
