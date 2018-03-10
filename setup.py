#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements/run.txt') as requirements_file:
    requirements = requirements_file.read()
    
with open('requirements/dev.txt') as dev_requires_file:
    setup_requirements = dev_requires_file.read()
    test_requirements = setup_requirements

setup(
    author="Matt Battifarano",
    author_email='mbattifa@andrew.cmu.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Urban data scraper is a framework for regularly scraping data from various sources",
    entry_points={
        'console_scripts': [
            'mac_data=mac_data.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mac_data',
    name='mac_data',
    packages=find_packages(include=['mac_data']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mbattifarano/mac_data',
    version='0.0.0',
    zip_safe=False,
)
