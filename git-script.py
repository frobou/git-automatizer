#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(
    description='My first argparse attempt',
    epilog='Example of use: git-auto.py -a|--action clone|sync')
parser.add_argument("-a", "--action", help="Ação requisitada", choices=['clone', 'sync'], default='sync')
parser.add_argument("-c", "--components", help="Vem com componentes", choices=['y', 'n'], default='n')
args = parser.parse_args()

from git_automatizer.frobouGit import FrobouGit

fgit = FrobouGit()

if args.action == 'sync':
    fgit.sync(args.components == 'y')
else:
    fgit.clone(args.components == 'y')
