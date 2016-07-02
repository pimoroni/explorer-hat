#!/bin/bash

gettools="yes"

if [ $gettools == "yes" ]; then
    sudo apt-get update && sudo apt-get install build-essential dh-make dh-python debhelper devscripts
    sudo apt-get install python-all python-setuptools python3-all python3-setuptools
fi

cd ..
debuild -Ipackage

exit 0
