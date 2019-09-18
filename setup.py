# -*- coding: utf-8 -*-

# mitschreiben
# ------------
# Python library supplying a tool to record values during calculations
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.3, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/mitschreiben
# License:  Apache License 2.0 (see LICENSE file)


import codecs

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

pkg = __import__('mitschreiben')

setup(
    name=pkg.__name__,
    description=pkg.__doc__,
    version=pkg.__version__,
    author=pkg.__author__,
    author_email=pkg.__email__,
    url=pkg.__url__,
    license=pkg.__license__,
    packages=find_packages(),
    package_data={pkg.__name__: list(pkg.__data__)},
    scripts=pkg.__scripts__,
    install_requires=pkg.__dependencies__,
    dependency_links=pkg.__dependency_links__,
    long_description='\n'+codecs.open('README.rst', encoding='utf-8').read(),
    platforms='any',
    classifiers=[
        'Development Status :: ' + pkg.__dev_status__,
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Education',
        'Topic :: Office/Business',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

