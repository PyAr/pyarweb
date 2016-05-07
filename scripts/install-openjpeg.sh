#!/bin/bash
# install openjpeg

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

command -v wget >/dev/null 2>&1 || { echo >&2 "I require wget but it's not installed.  Aborting."; exit 1; }

CURDIR=`pwd`

cd /tmp

if [ ! -f openjpeg-2.1.0.tar.gz ]; then
    wget 'http://iweb.dl.sourceforge.net/project/openjpeg.mirror/2.1.0/openjpeg-2.1.0.tar.gz'

fi

if [ ! -d openjpeg-2.1.0 ]; then
    rm -r openjpeg-2.1.0
fi

tar -xvzf openjpeg-2.1.0.tar.gz

pushd openjpeg-2.1.0

cmake -DCMAKE_INSTALL_PREFIX=/usr . && make -j4 && make install

popd

cd $CURDIR
