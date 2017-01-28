#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(
    description='git-automatizer by frobou',
    epilog='Exemplo de uso: git-auto.py -a|--action clone|sync')
parser.add_argument("-a", "--action", help="Ação requisitada", choices=['clone', 'sync'], default='sync')
parser.add_argument("-c", "--components", help="Vem com componentes", action='store_true', default=False)
parser.add_argument("-r", "--repository", help="So um repositorio")
args = parser.parse_args()

from git_automatizer.frobouGit import FrobouGit

fgit = FrobouGit()

if args.action == 'sync':
    fgit.sync(components=args.components, repository=args.repository)
else:
    fgit.clone(components=args.components, repository=args.repository)
