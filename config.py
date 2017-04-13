#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import argparse
from git_automatizer.frobouConfig import FrobouConfig

parser = argparse.ArgumentParser(prog='PROG')
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "a" command
parser_list = subparsers.add_parser('list', help='a help')
parser_list.add_argument("action", default='list')

# create the parser for the "a" command
parser_add = subparsers.add_parser('add', help='a help')
parser_add.add_argument("-action", default='add')
parser_add.add_argument("--opt1", action='store_true', required=True)
parser_add.add_argument("--opt2", action='store_true')

# create the parser for the "b" command
parser_del = subparsers.add_parser('del', help='b help')
parser_del.add_argument("--opt3", action='store_true')
parser_del.add_argument("--opt4", action='store_true', required=True)

args, remaining = parser.parse_known_args()

print(args)

if not remaining:
    print('list')
    exit(0)
if args.action:
    print('add')
elif 'del' in args:
    print('del')