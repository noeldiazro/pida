#!/usr/bin/env python

from distutils.core import setup, Extension

setup(name='Acquisition',
      version='1.0',
      description='piDA management software',
      author='Noel Diaz Rodriguez',
      author_email='noeldiazro@gmail.com',
      url='https://github.com/noeldiazro/piDA',
      py_modules=['Acquisition'],
      ext_modules=[
        Extension('clock',
                  ['src/pyclock.c', 'src/tsop.c'],
                  libraries=['rt']
                  ),
        Extension('spidev',
                  ['src/spidev_module.c']
                  )
        ],
      data_files=[('/etc', ['config/modules']),
                  ('/etc/modprobe.d', ['config/raspi-blacklist.conf'])
                  ]
      )
