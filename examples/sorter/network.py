from magma import *
from magma.bitutils import log2
from mantle import *
from swap import Swaps, swap
from permute import Riffle, UnRiffle, ReverseRiffle, UnReverseRiffle

# HalfCleaner
#
# Convert bitonic input into two bitonic halves
#
# Either the top half or the bottom half will be clean, all 0's or 1's
#
def HalfCleaner(n):
    if n == 2:
        return Swap()
    u = UnRiffle(n)
    s = Swaps(n)
    r = Riffle(n)
    return compose( u, compose( s, r ) )

def halfcleaner(I):
    return HalfCleaner(len(I))(I)

#
# ReverseHalfCleaner
#
# Convert 2 sorted inputs into two bitonic halves
#
def ReverseHalfCleaner(n):
    if n == 2:
        return Swap()
    u = UnReverseRiffle(n)
    s = Swaps(n)
    r = ReverseRiffle(n)
    return compose( u, compose( s, r ) )

def reversehalfcleaner(I):
    return ReverseHalfCleaner(len(I))(I)

#
# Convert a bitonic sequence into a sorted sequences
#
# HalfCleaner(n) => 2 BitonicSorter(n//2)
#
def DefineBitonicSorter(n):
    assert n in [2, 4, 8, 16]
    T = Bits(n)
    class _BitonicSorter(Circuit):
        name = 'BitonicSorter{}'.format(n)
        IO = ['I', In(T), "O", Out(T)]
        @classmethod
        def definition(io):
            if n == 2:
                wire(swap(io.I), io.O)
            else:
                halfcleaner = HalfCleaner(n)
                bitonic0 = BitonicSorter(n//2)
                bitonic1 = BitonicSorter(n//2)
                bitonic = flat( join(bitonic0, bitonic1), flatargs=['I','O'] )
                s = compose( bitonic, halfcleaner )
                wire( s(io.I), io.O )
    return _BitonicSorter

def BitonicSorter(n):
    return DefineBitonicSorter(n)()

def bitonicsorter(I):
    return BitonicSorter(len(I))(I)


#
# Merge 2 sorted sequencers into a sorted sequence
#
# 2 BitonicSorter(n/2) => ReverseHalfCleaner
#
def DefineMerger(n):
    assert n in [2, 4, 8, 16]
    T = Bits(n)
    class Merger(Circuit):
        name = 'Merger{}'.format(n)
        IO = ['I', In(T), "O", Out(T)]
        @classmethod
        def definition(io):
            if n == 2:
                wire(swap(io.I), io.O)
            else:
                revhalfcleaner = ReverseHalfCleaner(n)
                bitonic0 = BitonicSorter(n//2)
                bitonic1 = BitonicSorter(n//2)
                bitonic = flat( join(bitonic0, bitonic1), flatargs=['I','O'] )
                s = compose( bitonic, revhalfcleaner )
                wire( s(io.I), io.O )
    return Merger

def Merger(n):
    return DefineMerger(n)()

def merger(I):
    return Merger(len(I))(I)

#
# Convert an unsorted sequence into a sorted sequence
#
# 2 Sorters(n/2) => Merger(n) 
#
def DefineSorter(n):
    assert n in [2, 4, 8, 16]
    T = Bits(n)
    class _Sorter(Circuit):
        name = 'Sorter{}'.format(n)
        IO = ['I', In(T), "O", Out(T)]
        @classmethod
        def definition(io):
            if n == 2: # Sort 2 element sequences
                wire(swap(io.I), io.O)
            else:
                merger = Merger(n)
                sorter0 = Sorter(n//2) # bottom sorter 
                sorter1 = Sorter(n//2) # top sorter
                sorter = flat( join(sorter0, sorter1), flatargs=['I','O'] )
                s = compose( merger, sorter )
                wire( s(io.I), io.O )
    return _Sorter

def Sorter(n):
    return DefineSorter(n)()

def sorter(I):
    return Sorter(len(I))(I)
