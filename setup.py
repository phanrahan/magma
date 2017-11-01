from setuptools import setup
import sys
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects

install_requires = []
extra_requires = {}
for item in parse_requirements("requirements.txt", session=False):
    req = str(item.req)
    if item.markers is not None:
        req += ";" + str(item.markers)
    install_requires.append(req)

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
    install_requires=install_requires
)
