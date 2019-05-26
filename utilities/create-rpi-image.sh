#!/bin/bash
# https://www.raspberrypi.org/documentation/installation/installing-images/linux.md

SCRIPT_NAME=`basename "$0"`
RPI_VER="RetroPie-4.4"
RPI_FORM="P0"

USAGE="\n
Create Compressed Image from SD Card v1.1 \n
Joshua Eldridge (4/14/2019)\n
Usage: $SCRIPT_NAME sd_card_dev [output_filename]\n"

echo -e $USAGE

ERRORS[0]="**Wrong number of arguments provided. Script requires 1 or 2, $# provided.**"
ERRORS[1]="**Cannot stat SD Card {$SD_CARD}.**"

die () {
    echo >&2 "$@"
    exit 1
}

if [[ $# -eq 0 ]]; then
  die ${ERRORS[0]}
fi
SD_CARD=$1
# Minimum validation of the device
[ -e "$SD_CARD" ] || die ${ERRORS[1]}
if [[ -n $2 ]]; then
  sudo dd if=$SD_CARD bs=4M conv=fsync status=progress | gzip > $2
else
  IMG_DATE=`date +%Y%m%d`
  FILENAME=$IMG_DATE-$RPI_VER.$RPI_FORM
  sudo dd if=$SD_CARD bs=4M conv=fsync status=progress | gzip > $FILENAME.img.gz
fi
