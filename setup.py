#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Setup module for the Data Manager Job Utilities module
#
# February 2022

from setuptools import setup
import os

# Pull in the essential run-time requirements
with open('requirements.txt') as file:
    requirements = file.read().splitlines()


# Use the README.rst as the long description.
def get_long_description():
    return open('README.rst').read()


setup(

    name='im-data-manager-job-utilities',
    version=os.environ.get('GITHUB_REF_SLUG', '1.0.0'),
    author='Alan Christie',
    author_email='achristie@informaticsmatters.com',
    url='https://github.com/informaticsmatters/data-manager-job-utilities',
    license='MIT',
    description='Job execution utilities',
    long_description=get_long_description(),
    keywords='logging',
    platforms=['any'],

    # Our modules to package
    packages=['dm_job_utilities'],
    include_package_data=True,

    # Project classification:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: POSIX :: Linux',
    ],

    install_requires=requirements,

    zip_safe=False,

)
