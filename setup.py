#!/usr/bin/env python

from distutils.core import setup, Extension
setup(name='piDA',
      version='1.0',
      description='Data acquisition management software',
      author='Noel Diaz',
      author_email='noeldiazro@gmail.com',
      url='http://github.com/noeldiazro/piDA',
      packages=['piDA','piDA.interfaces','piDA.converters','piDA.links'],
      ext_modules=[
        Extension('clock', ['piDA/src/pyclock.c', 'piDA/src/tsop.c'], libraries=['rt']),
        Extension('spidev', ['piDA/src/spidev_module.c'])
      ],
      data_files=[
        ('/etc/modprobe.d',['piDA/config/raspi-blacklist.conf']),
        ('/etc',['piDA/config/modules'])
        ]
)
