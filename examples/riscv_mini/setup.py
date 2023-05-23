from setuptools import setup

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

DESCRIPTION = """\
Magma port of https://github.com/ucb-bar/riscv-mini
"""

setup(
    name='magma_riscv_mini',
    version='0.0.1',
    description=DESCRIPTION,
    scripts=[],
    packages=[
        "riscv_mini",
    ],
    install_requires=[
        "magma-lang>=2.1.19",
        "mantle",
        "mantle2",
        "fault"
    ],
    license='BSD License',
    url='https://github.com/leonardt/magma_riscv_mini',
    author='Leonard Truong',
    author_email='lenny@cs.stanford.edu',
    python_requires='>=3.7',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown"
)
