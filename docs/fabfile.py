#!/usr/bin/env python
from fabric.api import *
__requires__ = 'Sphinx==1.1.3'
import sys
from pkg_resources import load_entry_point

def build():
    local('python fabfile.py . _build')

if __name__ == '__main__':
    sys.exit(
        load_entry_point('Sphinx==1.1.3', 'console_scripts', 'sphinx-build')()
    )
