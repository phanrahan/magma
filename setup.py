from setuptools import setup
import sys

setup(
    name='magma',
    version='0.1',
    description='A circuit wiring language for programming FPGAs',
    scripts=['bin/magma'],
    packages=[
        "magma",
        "magma.frontend",
        "magma.backend",
        "magma.passes",
        "magma.simulator",
        "magma.testing"
    ],
    install_requires=[
        "six",
        "mako",
        "pyverilog",
        "numpy",
        "graphviz",
        "coreir",
        "bit_vector"
    ],
    python_requires='>=3.6'
)
