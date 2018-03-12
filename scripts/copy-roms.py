#!/usr/bin/python
import os
from os import path
from os import access
import sys
import shutil

files_to_copy = {}

games_list = '/home/pi/genesis-best.txt'
console = 'megadrive/'

input_rom_dir = '/home/pi/usb/home/pi/RetroPie/roms/'
output_rom_dir = '/home/pi/RetroPie/roms/'

binary_metadata_folders = {'snap/':'.mp4', 'wheel/':'.png', 'boxart/':'.png'}

in_console = input_rom_dir+console
out_console = output_rom_dir+console

# Validate the directories all exist as expected and are writable etc.
# Want to check that the intial directories exist first, as they are standard
# to RetroPie.

def validate_dirs(dir_list = []):
	for d in dir_list:
		if not path.exists(d):
			sys.exit('Directory ' + str(d) + ' does not exist! Check that the path is correct.')

	for d in dir_list:
		if not access(d, os.W_OK):
			sys.exit('Directory ' + str(d) + ' is not writable!')

validate_dirs([input_rom_dir, output_rom_dir, in_console, out_console])

for folder, extension in binary_metadata_folders.items():
	if not path.exists(out_console+folder):
		os.makedirs(out_console+folder)

# Now that the directories are all clear, process the input file
# with the list of games for the console.

# This function will take in the original rom name, with full system
# path and return the same with a new extension (like mp4)

def get_filename(romname, extension):
	return path.basename(path.splitext(romname)[0])+extension
	

games = open(games_list, 'r').read().splitlines()

for i in games:

	in_rom = in_console+i
	out_rom = out_console+i

	print "Copying ..."

	if not path.exists(out_rom):
		print in_rom + " to " + out_rom
		shutil.copyfile(in_rom, out_rom)
	else:
		print 'File ' + out_rom + ' exists. Skipping copy.'

	for folder,ext in binary_metadata_folders.items():
		metadata_file = get_filename(i, ext)
		in_filepath = in_console+folder+metadata_file
		out_filepath = out_console+folder+metadata_file
		if not path.exists(out_filepath):
			print in_filepath + " to " + in_filepath
			shutil.copyfile(in_filepath, out_filepath)
		else:
			print 'File ' + out_filepath + ' exists. Skipping copy.'
	
