#!/bin/env python3
# -*- coding: utf-8 -*-

import os

from automatizer.frobouGit import FrobouGit

fgit = FrobouGit()
print(fgit.pobrema(os.getcwd()))

print(os.listdir(path='.'))
