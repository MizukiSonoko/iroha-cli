#!/usr/bin/env python

from distutils.core import setup

setup(
      name='iroha-ya-cli',
      version='0.7',
      description='Cli for hyperledger/iroha',
      author='Sonoko Mizuki',
      author_email='mizuki.sonoko@gmail.com',
      packages=['src'],
      entry_points={
      'console_scripts':
            'iroha-ya-cli = src.main:main'
      },
)