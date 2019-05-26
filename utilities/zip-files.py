#!/usr/bin/env python

import os
import zipfile

directory = '.'

files = os.listdir(directory)

for f in files:
  if '.sfc' in f:
    basename,ext = os.path.splitext(f)
    with zipfile.ZipFile(basename+'.zip', 'w') as z:
        z.write(f)
        print f
        print basename + '.zip'
        os.remove(f)
