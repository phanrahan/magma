from __future__ import print_function
import traceback

def warn(*args):
    print(*args)
    traceback.print_stack()

def error(*args):
    print(*args)
    traceback.print_stack()
