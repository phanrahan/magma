from setuptools import setup

from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=False)

reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='magma',
    version='0.1-alpha',
    description='A circuit wiring language for programming FPGAs',
    packages=[
        "magma",
        "magma.backend"
    ],
    install_requires=reqs
    )
