# -*- coding: utf-8 -*-
from os.path import join, dirname
from setuptools import setup

version = 0.9

LONG_DESCRIPTION = """
Platron http://www.platron.ru/ is an online payment service provider.
This package provides basic tools for interaction with API.
"""

setup(name='platrontools',
      version=version,
      author='Alexey Kinyov',
      author_email='rudy@05bit.com',
      description='Python tools for Platron.ru',
      license='BSD',
      keywords='platron, api',
      url='https://github.com/05bit/python-platrontools',
      packages=['platrontools',],
      long_description=LONG_DESCRIPTION,
      install_requires=['requests',],
      classifiers=['Development Status :: 4 - Beta',
                   'Operating System :: OS Independent',
                   'License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Environment :: Web Environment',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',])
