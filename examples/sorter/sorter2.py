from magma import *
from network import halfcleaner, reversehalfcleaner, bitonicsorter, merger, sorter, Sorter, DefineSorter
from permute import Riffle, UnRiffle, ReverseRiffle, UnReverseRiffle, Reverse

#wire( Riffle(8)(main.J1), main.J3 )
#r = Riffle(8)
#u = UnRiffle(8)
#id = compose( u, r )

#r = ReverseRiffle(8)
#u = UnReverseRiffle(8)
#id = compose( u, r )

#wire( Reverse(8)(main.J1), main.J3 )
#r = Reverse(8)
#u = Reverse(8)
#id = compose( u, r )
#wire( id(main.J1), main.J3 )

#wire( halfcleaner(main.J1), main.J3 )
#wire( reversehalfcleaner(main.J1), main.J3 )

#wire( bitonicsorter(main.J1), main.J3 )

#wire( merger(main.J1), main.J3 )

#wire( sorter(main.J1), main.J3 )
main = DefineSorter(8)

