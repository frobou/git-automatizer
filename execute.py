# -*- coding: utf-8 -*-
import argparse
import getpass
import git
import os
import subprocess

parser = argparse.ArgumentParser(
    description='My first argparse attempt',
    epilog='Example of use: git-auto.py -s github -u erwt -p -r teste -m git -d asd')
parser.add_argument("-m", "--method", help="Protocolo utilizado", choices=['https', 'git'], default='git')
parser.add_argument("-a", "--action", help="Ação requisitada", choices=['clone', 'pass'], default='pass')
parser.add_argument("-r", "--repository", help="Repositrio remoto")
parser.add_argument("-d", "--destination", help="Destino local", default='')
parser.add_argument("-s", "--service", help="Informa o serviço utilizado", choices=['github', 'bitbucket'])
parser.add_argument("-u", "--username", help="Informa o nome do usuário", default=None)
parser.add_argument("-p", "--password", help="Informa o nome do usuário", action='store_false')
args = parser.parse_args()

if not args.repository:
    print('Informe o repositorio (-r|--repository nome do repositório)')
    exit(1)
if not args.service:
    print('Informe o serviço (-s|--service serviço)')
    exit(1)
if not args.username:
    print('Informe o nome de usuario (-r|--username nome do usuario)')
    exit(1)

if not args.username == None:
    if args.password == None:
        print('-p|--password must be informed')
        exit(1)
    pswd = getpass.getpass('Password:')

# todo: validar senhas estranhas
if pswd == '':
    print('password can not be empty')
    exit(1)
else:
    pswd = ':' + pswd