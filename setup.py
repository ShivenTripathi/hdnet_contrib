# -*- coding: utf-8 -*-
"""
    hdnet_contrib
    ~~~~~
    Hopfield denoising network setup file
"""

__version__ = "0.1"

from setuptools import setup

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
