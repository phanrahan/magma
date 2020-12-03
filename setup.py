from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='magma-lang',
    version='2.1.21',
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
        "magma.primitives",
        "magma.smart",
        "magma.simulator",
        "magma.syntax",
        "magma.syntax.transforms",
        "magma.ssa",
        "magma.testing",
        "magma.types"
    ],
    install_requires=[
        "colorlog",
        "astor",
        "six",
        "dataclasses",
        "mako",
        "pyverilog",
        "numpy",
        "graphviz",
        "coreir>=2.0.125",
        "hwtypes>=1.4.4",
        "ast_tools>=0.0.16",
        "staticfg"
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
