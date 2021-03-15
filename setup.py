#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="ictdrone",
    version="0.0.0",
    license="GPL",
    author="pycabbage",
    packages=["ictdrone"],
    package_dir={"ictdrone": "src"},
    description="ICT基礎ラボ用のOpenCVとtelloのラッパーモジュール",
    long_description=long_description,
    install_requires=open("requirements.txt").read().strip().splitlines(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Natural Language :: Japanese",
        "Topic :: Utilities",
    ]
)
