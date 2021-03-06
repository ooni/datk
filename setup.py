from __future__ import print_function

try:
    from setuptools import setup, find_packages
    extra = {}
except ImportError:
    from distutils.core import setup, find_packages
    extra = {}

import sys

from oonidatk import __version__

def readme():
    try:
        with open('Readme.md') as f:
            return f.read()
    except:
        return ''

setup(name = 'oonidatk',
      version = __version__,
      description = 'OONI Data Analysis Toolkit',
      long_description = readme(),
      author = 'Open Observatory of Network Interference (OONI)',
      author_email = 'contact@openobservatory.org',
      scripts = [],
      url = 'https://github.com/ooni/datk/',
      packages = find_packages(),
      license = 'BSD-2-Clause',
      platforms = 'Posix; MacOS X; Windows',
      classifiers = ['Development Status :: 2 - Pre-Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: OS Independent',
                     'Topic :: Internet',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.3',
                     'Programming Language :: Python :: 3.4'],
      **extra
      )
