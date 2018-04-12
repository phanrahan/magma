from setuptools import setup
import sys

setup(
    name='magma',
    version='0.1-alpha',
    description='A circuit wiring language for programming FPGAs',
    scripts=['bin/magma'],
    packages=[
        "magma",
        "magma.backend",
        "magma.passes",
        "magma.simulator",
        "magma.testing"
    ],
    install_requires=[
        "six",
        "mako",
        "pyverilog",
        "backports-functools-lur-cache;python_vesion < '3'",
        "funcsigs;python_vesion < '3.3'",
        "numpy",
        "graphviz",
        "coreir",
        "bit_vector"
    ],
    python_requires='>=3.6'
)
