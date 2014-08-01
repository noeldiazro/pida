#!/bin/bash
if [[ $1 != --no-update ]] ; then
	sudo apt-get update
fi
sudo apt-get install python-dev
sudo python setup.py install
