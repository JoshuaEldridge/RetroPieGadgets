#!/bin/bash
# https://github.com/mickelson/attract/wiki/Compiling-on-the-Raspberry-Pi-(Raspbian-Jessie)

# Compiling Attract-Mode from source on the RaspberryPi 3
# When installing via the RetroPie-Setup experimental packages
# option hardware acceleration (mmal) is not available for video preview.
# This method will enable it.

if [ "$EUID" -ne 0 ]
  then echo "This script must be run as root."
  exit
fi

# Get and install system updates
sudo apt-get update
sudo apt-get upgrade

# Create a build environment
cd ~
mkdir develop

# Install "sfml-pi" and Attract-Mode dependencies

sudo apt-get install cmake libflac-dev libogg-dev libvorbis-dev libopenal-dev libfreetype6-dev libudev-dev libjpeg-dev libfontconfig1-dev

# Download and build sfml-pi

cd ~/develop
git clone --depth 1 https://github.com/mickelson/sfml-pi sfml-pi
mkdir sfml-pi/build
cd sfml-pi/build
cmake .. -j4 -DSFML_RPI=1 -DEGL_INCLUDE_DIR=/opt/vc/include -DEGL_LIBRARY=/opt/vc/lib/libbrcmEGL.so -DGLES_INCLUDE_DIR=/opt/vc/include -DGLES_LIBRARY=/opt/vc/lib/libbrcmGLESv2.so
sudo make install
sudo ldconfig

# Build FFmpeg with mmal support (hardware accelerated video decoding)

cd ~/develop
git clone --depth 1 git://source.ffmpeg.org/ffmpeg.git
cd ffmpeg
./configure --enable-mmal --disable-debug --enable-shared
make -j4
sudo make install
sudo ldconfig

# Download and build Attract-Mode

cd ~/develop
git clone --depth 1 https://github.com/mickelson/attract attract
cd attract
make -j4 USE_GLES=1
sudo make install USE_GLES=1

# Clean up
cd ~
rm -r -f ./develop

sudo reboot