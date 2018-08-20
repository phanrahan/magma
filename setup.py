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
        "zenlog",
        "astor",
        "six",
        "mako",
        "pyverilog",
        "numpy",
        "graphviz",
        "fault==0.19",
        "coreir==0.23a0",
        "bit_vector==0.30a0"
    ],
    python_requires='>=3.6'
)
