=== Types ===

Bit - primitive type

Array(n,T) - construct an array with n elements of type T
   Array2 = Array(2, Bit)
   array2 = Array2()
   constructor: array2 = Array2(1, 0)
   selectors: array2[0], array2[1]

Tuple(a1, T1, ..., an, Tn) - consruct a tuple with named elements
   Tuple2 = Tuple("x", Bit, "y", Bit)
   tuple = Tuple2()
   constructor: tuple2 = Tuple2(0,1)
   selectors: tuple2.x, tuple2.y

type name T - associate name with T
   type Point Tuple(x, Bit, y, Bit)


==== Nodes ====

primitive name(*args)
   
circuit name(*args)
endcircuit

name instname

wire port1 to port2

e.g.
    primitive Buf(input I Bit, output O Bit)

    circuit Nop(input I Bit, output O Bit)
    Buf buf;
    wire I to buf.I
    wire buf.O to O
    endcircuit



