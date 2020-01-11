import sexpr
import sys
import os
from pprint import pprint
from subprocess import Popen, PIPE

fname = sys.argv[1]
name = os.path.basename(fname).split('.')[0]
file = open(fname)

source = ""
for line in file.readlines():
  if line[0] != "#":
    source += line
sexpr.input(source)
s = sexpr.parse()
while len(s) == 1:
    s = s[0]
table = {}
for x in s:
  table[x[0]] = x[1:]

class Element():
  def __init__(self,name):
    self.name = name
    self.cfg = []
    self.inputs = []
    self.outputs = []
  def canelide(self):
    if len(self.cfg) == 0:
      if len(self.inputs) == 0 and len(self.outputs) == 1:
        return self.outputs[0] == self.name
      elif len(self.inputs) == 1 and len(self.outputs) == 0:
        return self.inputs[0] == self.name 
    return False 
class Primitive():
  def __init__(self,sexpr):
    self.name = sexpr[1]
    #pprint(sexpr)
    input,output = Element("input"),Element("output")
    self.elements = [ input, output ]
    self.connections = {} # (e0,outputpin,e1,inputpin) => true
    for i in sexpr[4:]:
      if i[0] == "pin":
        if i[3] == "input":
          input.outputs.append(i[2])
          self.connections[ ("input",i[2],i[1],i[2]) ] = True
        else:
          output.inputs.append(i[2]) 
          self.connections[ (i[1],i[2],"output",i[2]) ] = True
      elif i[0] == "element":
        e = Element(i[1])
        self.elements.append(e)
        for ii in i[2:]:
          if isinstance(ii,list):
            if ii[0] == "pin":
              getattr(e,ii[2]+"s").append(ii[1])
            elif ii[0] == "conn":
              if ii[3] == "==>":
                self.connections[ (ii[1],ii[2],ii[4],ii[5]) ] = True
              else:
                self.connections[ (ii[4],ii[5],ii[1],ii[2]) ] = True
            elif ii[0] == "cfg":
                e.cfg = ii[1:]
    
  def save(self):
    print("Saving %s" % self.name)
    p = Popen(["dot","-Tpdf","-o","%s_%s.pdf" % (self.name,name)], stdin=PIPE)
    f = p.stdin
    def write(s):
      f.write(s)
      if self.name == "PCIE_3_0":
        sys.stdout.write(s)
      
    write("digraph G {\n")
    write("    graph [rankdir = LR];\n")
    write("    node[shape=record];\n")
    
    for e in self.elements:
      def namefmt(xs):
        return "|".join([ "<%s>%s" % (x,x) for x in xs])
      def quote(x):
        return """ \\"%s\\" """ % x.replace("<","\\<").replace(">","\\>").replace("|","\\|")
      cfgstring = '\\n'.join([quote(x) for x in e.cfg])
      if e.canelide():
        write("""    %s[label="<%s>%s"];\n""" % (e.name,e.name,e.name))
      else:
        write("""    %s[label="{ {%s} | %s\\n%s | {%s} }"];\n""" % (e.name,namefmt(e.inputs),e.name,cfgstring,namefmt(e.outputs)))
    
    for t in self.connections.keys():
      write("    %s:%s -> %s:%s;\n" % t)
      
    write("}")
    f.close()
    if p.wait() != 0:
      raise 
    

for i in table["primitive_defs"]:
  if i[0] == "primitive_def":
    p = Primitive(i)
    try:
      p.save()
    except:
      print("Failed to save %s" % p.name)
