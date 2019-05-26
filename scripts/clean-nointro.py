#!/usr/bin/python

import os

#roms_dir = '/media/josh/NTFS450GB/retropie/NoIntro2018/No-Intro 2018/snes'

roms_dir = '/media/josh/NTFS450GB/retropie/NoIntro2018/No-Intro 2018/nes'
for file in os.listdir(roms_dir):
    #if os.path.isfile(file):
    if "USA" not in file or "Beta" in file or "Proto" in file or "Rev " in file:
        if os.path.isfile(os.path.join(roms_dir,file)):
            os.remove(os.path.join(roms_dir,file))
            print file
