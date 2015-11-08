#!/usr/bin/env python

from setuptools import setup
import station

setup(
    name='station',
    version=station.__version__,
    description='context manager computational engines',
    author='freeman-lab',
    author_email='the.freeman.lab@gmail.com',
    packages=['station'],
    url='https://github.com/freeman-lab/station',
    install_requires=open('requirements.txt').read().split(),
    long_description='See https://github.com/freeman-lab/station'
)
