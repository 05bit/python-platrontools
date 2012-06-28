# -*- coding: utf-8 -*-
from os.path import join, dirname
from setuptools import setup

version = 0.9

LONG_DESCRIPTION = """
Python tools for Platron (http://platron.ru) service API
"""

setup(name='platrontools',
      version=version,
      author='Alexey Kinyov',
      author_email='rudy@05bit.com',
      description='Python tools for Platron.ru',
      license='BSD',
      keywords='platron, api',
      url='https://bitbucket.org/05bit/py-platrontools',
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
