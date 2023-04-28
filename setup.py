#!/usr/bin/env python3
from setuptools import setup

setup(
    name='slackbot',
    version=0.1,
    author='Barakat Ajadi',
    author_email='babiola-ctr@wikimedia.org',
    license='Apache 2.0',
    description='run performance tests',
    packages=[
        'slackbot'
    ],
    install_requires=[
        'flask',
        'slackeventsapi',
        'slack',
        'python-dotenv',
        'slackclient'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
    }
)
