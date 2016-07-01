#!/bin/bash

gettools="yes"

if [ $gettools == "yes" ]; then
    sudo apt-get update && sudo apt-get upgrade
    sudo apt-get install devscripts debhelper
    sudo apt-get install python-all python-setuptools
    sudo apt-get install python3-all python3-setuptools
fi

debuild -Ipackage

exit 0
