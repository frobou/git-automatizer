#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import argparse
from git_automatizer.frobouConfig import FrobouConfig

mesg = 'Example of use: git-auto.py -a|--action add|del|list'
parser = argparse.ArgumentParser(
    description='git-automatizer by frobou - configurator',
    epilog=mesg)
parser.add_argument("-a", "--action", help="Ação requisitada", choices=['add', 'del', 'list'], default='list')
parser.add_argument('-r', '--repository')
parser.add_argument('-s', '--service')
parser.add_argument('-u', '--username')
parser.add_argument('-p', '--password')
parser.add_argument('-k', '--ssh_key')
parser.add_argument('-m', '--method')
parser.add_argument('-d', '--destination')
args = parser.parse_args()

g = FrobouConfig()

if args.action == 'list':
    g.repo_list()
    exit(0)
elif args.action == 'add':
    mesg = 'Example of use: git-auto.py -a add -r repo -s github'
    add_parser = argparse.ArgumentParser(
        description='git-automatizer by frobou - configurator',
        epilog=mesg)
    add_parser.add_argument('-a', '--action')
    add_parser.add_argument('-r', '--repository', help='Repositorio', required=True)
    add_parser.add_argument('-s', '--service', help='Serviço', required=True)
    add_parser.add_argument('-u', '--username', help='Username', default=None)
    add_parser.add_argument('-p', '--password', help='Password', action='store_true', default=None)
    add_parser.add_argument('-k', '--ssh_key', help='Chave ssh', action='store_true', default=False)
    add_parser.add_argument('-m', '--method', help='Pasta destino', choices=['ssh', 'https'], default='ssh')
    add_parser.add_argument('-d', '--destination', help='Pasta destino', default=None)
    add_args = add_parser.parse_args()
    if add_args.password:
        add_args.password = getpass.getpass('Password: ')
    g.add_project(repo=add_args.repository, service=add_args.service, protocol=add_args.method,
                  username=add_args.username, password=add_args.password,
                  ssh_key=add_args.ssh_key, to_foler=add_args.destination)
else:
    mesg = 'Example of use: git-auto.py -a del -r repo'
    del_parser = argparse.ArgumentParser(
        description='git-automatizer by frobou - configurator',
        epilog=mesg)
    del_parser.add_argument('-a', '--action')
    del_parser.add_argument('-r', '--repository', help='Repositorio', required=True)
    del_args = del_parser.parse_args()
    g.remove_project(del_args.repository)
