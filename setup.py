from setuptools import setup
import sys

setup(
    name='magma-lang',
    version='0.1.4',
    url='https://github.com/phanrahan/magma',
    license='MIT',
    maintainer='Lenny Truong',
    maintainer_email='lenny@cs.stanford.edu',
    description='An embedded DSL for constructing hardware circuits',
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
        "coreir==0.30a0",
        "bit_vector==0.39a0"
    ],
    python_requires='>=3.6'
)
