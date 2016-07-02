#!/bin/bash

gettools="yes"
cleanup="yes"

if [ $gettools == "yes" ]; then
    sudo apt-get update && sudo apt-get install build-essential dh-make dh-python debhelper devscripts
    sudo apt-get install python-all python-setuptools python3-all python3-setuptools
fi

cd ../library
debuild -Ipackage

mv ../*.build ../packaging
mv ../*.changes ../packaging
mv ../*.tar.xz ../packaging
mv ../*.deb ../packaging
mv ../*.dsc ../packaging

if [ $cleanup == "yes" ]; then
    dh clean
    rm -R ./build
fi

exit 0
