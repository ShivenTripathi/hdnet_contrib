# -*- coding: utf-8 -*-
"""
    hdnet_contrib
    ~~~~~
    Hopfield denoising network setup file
"""

__version__ = "0.1"

from setuptools import setup
import os

hook = "README.md"
path = os.path.abspath(hook)
pathDir = path.replace(hook,'')
pathDir += "hdnet_contrib/PyCDMentropy/CDMentropy"
pathFile = path.replace(hook,'')
pathFile += "hdnet_contrib/CDMentropy.py"
line = "DEFAULT = \""+pathDir+"\"" 
with open (pathFile, 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(line.rstrip('\r\n') + '\n' + content)

setup(
    name='hdnet_contrib',
    version=__version__,
    description='Repository for HDNet\'s extra modules',
    url='http://github.com/',
    author='Shiven Tripathi',
    author_email='shiven@iitk.ac.in',
    license='GPLv3',
    packages=['hdnet_contrib'],
    install_requires=[
        'hdnet',
        'oct2py'
    ],
    zip_safe=False)
