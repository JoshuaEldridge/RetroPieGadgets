#!/bin/bash
#https://stackoverflow.com/questions/699576/validating-parameters-to-a-bash-script#699613

SCRIPT_NAME=`basename "$0"`
USAGE="\n
Burn Compressed Image to SD Card v1.1 \n
Joshua Eldridge (4/14/2019)\n
Usage: $SCRIPT_NAME input_filename sd_card_dev\n"

echo -e $USAGE

ERRORS[0]="**Wrong number of arguments provided. Script requires 2, $# provided.**\n"
ERRORS[1]="**Can't find the SD Card image as provided {$IMG_FILE}.**\n"
ERRORS[2]="**Cannot stat SD Card {$SD_CARD}.**\n"

die () {
    echo -e >&2 "$@"
    exit 1
}


if [[ $# -lt 2 ]]; then
  die ${ERRORS[0]}
fi
IMG_FILE=$1
SD_CARD=$2

# Minimum validation that image and device exist
[ -e "$IMG_FILE" ] || die ${ERRORS[1]}
[ -e "$SD_CARD" ] || die ${ERRORS[2]}

sudo gzip -dc $IMG_FILE | sudo dd of=$SD_CARD bs=4M status=progress
