# -*- coding: utf-8 -*-
# @Author: prabhakar
# @Date:   2016-06-25 20:13:13
# @Last Modified by:   Prabhakar Gupta
# @Last Modified time: 2016-06-25 20:16:48

from setuptools import setup

setup(name='github_email',
    version='0.0.1',
    description='Get email ID of any GitHub user',
    long_description='Get a list of email IDs of any valid GitHub user from one function call even if there are no public email for that user',
    keywords='github email user public commit get',
    url='http://github.com/prabhakar267/github_email',
    author='Prabhakar Gupta',
    author_email='prabhakargupta267@gmail.com',
    license='MIT',
    packages=['github_email'],
    install_requires=['requests', 'json'],
    zip_safe=False)