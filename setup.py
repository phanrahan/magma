from setuptools import setup
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='magma-lang',
    version='1.0.3',
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
        "magma.syntax",
        "magma.ssa",
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
        "coreir>=2.0.*",
        "hwtypes>=1.0.*"
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
