from distutils.core import setup, Extension

setup(name='tsop',
      ext_modules=[
        Extension('tsop',
                  ['pytsop.c', 'tsop.c'],
                  libraries=['rt']
                  )
        ]
)
