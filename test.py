# -*- coding: utf-8 -*-
import argparse
import os.path
import paramiko
import json
import sys

# print(sys.version_info.major)

config = {'handler': 'adminhandler.py', 'timeoutsec': 5}
home = os.path.expanduser('~')

# print(os.path.isdir('{}/config.json'.format(home)))

json.dump(config, open('{}/config.json'.format(home), 'w'))
a = json.load(open('{}/config.json'.format(home)))
# print(a['handler'])

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Informa o arquivo a ser comprimido", default='test.py')
parser.add_argument("-m", "--mode", help="Informa o modo de compressão", choices=['bao', 'opa', 'eita'], default='bao')
args = parser.parse_args()

if not args.file:
    print('Informe o arquivo (-f arquivo ou --file arquivo)')
    exit(1)

if not os.path.isfile(args.file):
    print('Arquivo informado não encontrado: ({})'.format(args.file))
    exit(1)

ssh = paramiko.client.SSHClient()
ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
ssh.load_system_host_keys()
try:
    ssh.connect('127.0.0.1', compress=True, password='esqueci')
    ssh.invoke_shell()
    stdin, stdout, stderr = ssh.exec_command('dnf update', get_pty=True)
except paramiko.ssh_exception.AuthenticationException as e:
    print('Invalid user or password')
    exit(1)

for l in stdout.readlines():
    print(l)

ssh.close()
