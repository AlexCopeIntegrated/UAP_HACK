#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="rtlsdr_tool",
    version="0.1.0",
    description="A command-line utility for capturing and processing RTL-SDR radio data",
    author="RTL-SDR Tool Authors",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "rtlsdr-tool=rtlsdr_tool.cli:main",
        ],
    },
    install_requires=[
        "numpy>=1.20.0",
        "pyrtlsdr>=0.2.9",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications :: Ham Radio",
        "Topic :: Scientific/Engineering",
    ],
)
