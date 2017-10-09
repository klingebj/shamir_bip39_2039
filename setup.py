# !/usr/bin/env python

from setuptools import setup
setup(
    name='shamir_bip39_2039',
    version='0.0.1',
    test_suite='nose2.collector.collector',
    packages=['shamir_bip39_2039'],
    package_data={'shamir_bip39_2039': ['english.txt']})
