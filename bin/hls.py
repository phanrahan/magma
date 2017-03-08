import sys
import subprocess as sp
import os

cd = os.path.join

def run(x): sp.call(x, shell = True)

basename = sys.argv[1]

rhea_target = "%s_hls.ss" % basename
rhea_exe_base = cd(os.getenv("MAGMA_BIN"), "rhea-hls")

if sys.platform in ['darwin']:
    rhea_exe = rhea_exe_base
if sys.platform in ['win32', 'win64', 'nt']:
    rhea_exe = rhea_exe_base + ".exe"

print ("%s %s > %s" % (rhea_exe, basename + ".ss", rhea_target))
run("%s %s > %s" % (rhea_exe, basename + ".ss", rhea_target))

print("makecpu %s" % basename + "_hls")
run("makecpu %s" % basename + "_hls")

