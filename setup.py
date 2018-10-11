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
        "colorlog",
        "astor",
        "six",
        "mako",
        "pyverilog",
        "numpy",
        "graphviz",
        "coreir==0.27a0",
        "bit_vector==0.37a0"
    ],
    python_requires='>=3.6'
)
