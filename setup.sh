#!/bin/bash

sudo apt-get update
sudo apt-get install python-dev
cp setup.py ..
cd ..
sudo python setup.py install
