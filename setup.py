#!/usr/bin/env python

import os

from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name="psphere",
      version="0.5.3",
      description="vSphere SDK for Python",
      long_description=read("README.rst"),
      author="Jonathan Kinred  / Matt Welch",
      author_email="jonathan.kinred@gmail.com / intr1nsic@tallshorts.com",
      url="http://bitbucket.org/intr1nsic/omoto",
      packages=["psphere"],
      package_data={"psphere": ["wsdl/*", "aobjects/*", "network/*"]},
      install_requires=["suds", "PyYAML"],
      keywords=["vsphere", "vmware"],
      classifiers=["Development Status :: 4 - Beta",
                   "License :: OSI Approved :: Apache Software License"],
     )
