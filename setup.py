#!/usr/bin/env python
"""
pida
----

pida is a library to manage data acquisition hardware
from Raspberry Pi
"""
from setuptools import setup, Extension

setup(
    name='pida',
    version='0.1',
    url='https://github.com/noeldiazro/piDA',
    license='BSD',
    description='Data acquisition management software',
    long_description=__doc__,
    author='Noel Diaz Rodriguez',
    author_email='noeldiazro@gmail.com',
    packages=['pida'],
    include_package_data=True,
    install_requires=[
        'spidev'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
    ext_modules=[
        Extension('clock', ['piDA/src/pyclock.c', 'piDA/src/tsop.c'], libraries=['rt'])
    ]
    #data_files=[
    #    ('/etc/modprobe.d',['config/raspi-blacklist.conf']),
    #    ('/etc',['config/modules'])
    #]
)

__author__ = 'Noel Diaz Rodriguez'
