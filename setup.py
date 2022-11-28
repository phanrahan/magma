from distutils.version import LooseVersion
import multiprocessing
import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import sys


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Release'
        build_args = ['--config', cfg]

        cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]

        cpu_count = max(2, multiprocessing.cpu_count() // 2)
        build_args += ['--', '-j{0}'.format(cpu_count)]

        python_path = sys.executable
        cmake_args += ['-DPYTHON_EXECUTABLE:FILEPATH=' + python_path]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args,
                              cwd=self.build_temp)

        subprocess.check_call(
            ['cmake', '--build', '.'] + build_args,
            cwd=self.build_temp)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='magma-lang',
    version='2.2.44',
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
        "magma.backend.coreir",
        "magma.backend.mlir",
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
    ext_modules=[CMakeExtension("magma_debug", 'debug-ext')],
    cmdclass=dict(build_ext=CMakeBuild),
    install_requires=[
        "colorlog",
        "astor",
        "six",
        "dataclasses",
        "mako",
        "pyverilog",
        "numpy",
        "graphviz",
        "coreir>=2.0.151",
        "hwtypes>=1.4.4",
        "ast_tools>=0.0.16",
        "staticfg",
        "networkx",
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
