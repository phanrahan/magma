import sys
import subprocess as sp
import os

cd = os.path.join

def run(x): sp.call(x, shell = True)

basename = sys.argv[1]

cpugen_target = "%s.py" % basename
cpugen_footer = "%s_footer.py" % basename

cpugen_exe_base = cd(os.getenv("MAGMA_BIN"), "cpugen")

if sys.platform in ['darwin']:
    cpugen_exe = cpugen_exe_base
if sys.platform in ['win32', 'win64', 'nt']:
    cpugen_exe = cpugen_exe_base + ".exe"

print ("%s %s > %s" % (cpugen_exe, basename + ".ss", cpugen_target))
run("%s %s > %s" % (cpugen_exe, basename + ".ss", cpugen_target))
run("cat %s >> %s" % (cpugen_footer, cpugen_target))
run("sh makev %s" % basename)



