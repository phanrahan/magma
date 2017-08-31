"""
Adapted from https://github.com/ddm/icetools
"""

from sys import platform
from subprocess import call
import os
import argparse

parser = argparse.ArgumentParser(description='Install the toolchain for programming the icestcik')
parser.add_argument('--num_cores', type=int, default=1,
                   help='run make with `num_cores` cores (-j `num_cores`)')
args = parser.parse_args()

apt_packages = ["pkg-config", "build-essential", "bison", "flex", "gawk",
        "tcl-dev", "libffi-dev", "git", "mercurial", "python", "python3",
        "libftdi-dev", "libreadline-dev", "clang", "graphviz", "xdot"]

brew_packages = ["python3", "libftdi0", "libffi", "autoconf", "bison", "gawk",
        "gnu-sed", "graphviz", "xdot", "mercurial"]


def run(command):
    print(" ".join(command))
    call(command)


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


print("Installing third party dependencies")
if platform == "linux" or platform == "linux2":
    linux_distribution = platform.linux_distribution()[0]
    if "ubuntu" in linux_distribution:
        run(["sudo", "apt-get", "install", "-y"] + apt_packages)
    else:
        raise NotImplementedError(linux_distribution)
elif platform == "darwin":
    run(["brew", "install"] + brew_packages)
elif platform == "win32":
    raise NotImplementedError("Windows")

def install(package, url):
    if os.path.isdir(package):
        print("{} directory exists, assuming it is a clone of {} and updating...".format(package, url))
        with cd(package):
            run(["git", "pull", "origin", "master"])
    else:
        run(["git", "clone", url, package])

    with cd(package):
        run(["make", "clean"])
        run(["make", "-j", str(args.num_cores)])
        if platform == "linux" or platform == "linux2":
            run(["sudo", "make", "install"])
        else:
            run(["make", "install"])

install("icestorm", "https://github.com/cliffordwolf/icestorm.git")
install("yosys", "https://github.com/cliffordwolf/yosys.git")
install("arachne-pnr", "https://github.com/cseed/arachne-pnr.git")
