#!/usr/bin/python
import os
from os import path
from os import access
import sys
import shutil
import argparse

class is_readable(argparse.Action):
    def __call__(self, parser, namespace, values, mode, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentError(self, "is_readable: {0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentError(self, "is_readable: {0} is not a readable directory".format(prospective_dir))

class is_writable(argparse.Action):
    def __call__(self, parser, namespace, values, mode, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentError(self, "is_writable: {0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.W_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentError(self, "is_writable: {0} is not a writable directory".format(prospective_dir))

parser = argparse.ArgumentParser(fromfile_prefix_chars='@',
                                     description="This program will reference a file containing a list of roms and copy those roms and all of the associated metadata from a specified metadata from one location to another.")
parser.add_argument("-f", "--filename", type=argparse.FileType('r'), required=True,
                    help="path to file containing the list of games")
parser.add_argument("-c", "--console", choices=['nes', 'snes', 'genesis'], required=True,
                    help="name of the console folder")
parser.add_argument("-i", "--input_dir", required=True, action=is_readable,
                    help="name of the root folder for roms and metadata (eg: /usb/roms/)")
parser.add_argument("-o", "--output_dir", action=is_writable,
                    help="name of the console folder (eg: /home/pi/RetroPie/roms/)")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="print progress and output to screen")

args = parser.parse_args()

args.filename
args.console
args.input_dir
args.output_dir

#in_console = path.join(args.input_dir, args.console)
in_console = args.input_dir
out_console = path.join(args.output_dir, args.console)

# This function will take in the original rom name, with full system
# path and return the same with a new extension (like mp4)

def get_filename(romname, extension):
    return path.basename(path.splitext(romname)[0])+extension

files_to_copy = {}

#binary_metadata_folders = {'snap/':'.mp4', 'wheel/':'.png', 'boxart/':'.png', 'images/':'.png'}
binary_metadata_folders = {}

for folder, extension in binary_metadata_folders.items():
    if not path.exists(path.join(out_console,folder)):
        os.makedirs(path.join(out_console,folder))
        print 'creating folder: ' + str(path.join(out_console,folder))

# Now that the directories and permissions are all clear, process the input file
# with the list of games for the console.

games = args.filename.read().splitlines()

for i in games:

    in_rom = path.join(in_console, i)
    out_rom = path.join(out_console, i)

    print "Copying ..."

    if not path.exists(out_rom) and path.exists(in_rom):
        print in_rom + " to " + out_rom
        shutil.copyfile(in_rom, out_rom)
    else:
        print 'Error: ' + out_rom + ' exists. Or ' + in_rom + ' not found. Skipping copy.'

    for folder, ext in binary_metadata_folders.items():
        metadata_file = get_filename(i, ext)
        in_filepath = path.join(in_console, folder, metadata_file)
        out_filepath = path.join(out_console, folder, metadata_file)
        if not path.exists(out_filepath):
            print in_filepath + " to " + in_filepath
            if path.exists(in_filepath):
                shutil.copyfile(in_filepath, out_filepath)
            else:
                print 'File ' + in_filepath + ' not found.'
        else:
            print 'File ' + out_filepath + ' exists. Skipping copy.'
