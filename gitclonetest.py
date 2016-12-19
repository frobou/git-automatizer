# -*- coding: utf-8 -*-

from automatizer.frobouGit import FrobouGit

fgit = FrobouGit()
# fgit.clone(True) # com instalacao dos componentes
# fgit.clone() # sem instalacao dos componente
fgit.sync()

print(fgit.getResult())
