#!/usr/bin/python
from __future__ import print_function
import lxml.etree as e
import re
import os
from shutil import copyfile

# This script will attempt to read a complete gamelist.xml file formatted
# for Emulation Station and copy all of the associated assets into the correct
# destimation locations.

# If you want to check the current structure of assets in the
# gamelist.xml file first, set dry run to True
dry_run = False

# the base directory location where the assets will be read from
# roms should be in the root, media asset folders will be mapped using
# the asset_locations dictionary below if they aren't the same as the
# gamelist.xml standard
src_directory = '/home/josh/Downloads/retropie/roms/nes/'

# the target directory to write assets to, this can be completely different
# from the source gamelist directory

dest_directory = '/home/josh/Downloads/retropie/'

source_gamelist = '/home/josh/Downloads/retropie/gamelist.xml'

# use this to change the destination folder names
# the format of this packed dictionary is {"xml tag name": ["old name", "new name"]}
#asset_locations = {"image":["screenshots", "ss"], "marquee":["marquees", "m"], "video":["video", "v"]}

clean_name = True

asset_tags = ['path', 'image', 'marquee', 'video']
display_tags = ['name', 'path', 'image', 'marquee', 'video']

def clean_nointro_name(old_name):
    return re.sub(r'[\s]*\([^)]*\)', '', old_name)

def check_read(dir):
    if not os.path.isdir(dir):
        raise ValueError('check_perms(): ' + dir + ' is not a valid path')
    if not os.access(dir, os.R_OK):
        raise ValueError('check_perms(): ' + dir + ' is not readable')

def check_write(dir):
    if not os.path.isdir(dir):
        raise ValueError('check_perms(): ' + dir + ' is not a valid path')
    if not os.access(dir, os.W_OK):
        raise ValueError('check_perms(): ' + dir + ' is not writable')

def clean_rel_path(in_path):
    if in_path[:2] == './':
        return in_path.replace('./', '')
    else:
        return in_path

# =================== #

check_read(src_directory)
check_write(dest_directory)

tree = e.parse(source_gamelist)

root = tree.getroot()
if dry_run is True:
    for child in root:
        for i in child:
            if i.tag in display_tags:
                print(i.tag, i.text)
    exit(1)
else:
    for child in root:
        for i in child:

            if i.tag in asset_tags and i.text is not None:
                file_path, file_basename = os.path.split(i.text)

                src_filepath = os.path.join(src_directory, file_path, file_basename)
                dest_filepath = os.path.join(dest_directory, file_path, file_basename)
                if os.path.isfile(src_filepath) and not os.path.isfile(dest_filepath):
                    copyfile(src_filepath, dest_filepath)
                    print('Copied: ', src_filepath)
                    print('To: ', dest_filepath)
                else:
                    print('Error: Source file not found or destination file already exists!')
                    print(src_filepath)
                    print(dest_filepath)

# if __name__ == "__main__":
#     # execute only if run as a script
#     main()
