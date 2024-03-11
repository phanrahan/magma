import magma as m


class FullAdder(m.Circuit):
    # Interface ports are declared using the m.IO object
    # A port has a name (appears before the =) and a type (appears after
    # the =)
    # The type must have a direction (In, Out, or InOut)
    io = m.IO(
        a=m.In(m.Bit),
        b=m.In(m.Bit),

        cin=m.In(m.Bit),
        sum_=m.Out(m.Bit),
        cout=m.Out(m.Bit)
    )
    # We can assign references to output wires to temporary python
    # variables (in this case, a_xor_b refers to the output of the XOr

    # circuit instanced by using the `^` (xor) operator)

    a_xor_b = io.a ^ io.b
    # To wire the output of an instance (e.g. the output of the instance
    # created by a_xor_b ^ cin) to an output port (sum_), we use the `@=`
    # operator
    io.sum_ @= a_xor_b ^ io.cin

    # Here's another example of assignment (for python variables) and
    # wiring (for magma ports).  We assign three temporaries for the
    # outputs of various & (and) operators.  Then we wire the result of
    # "or"ing (|) these together to the `cout` output port
    a_and_b = io.a & io.b
    b_and_cin = io.b & io.cin
    a_and_cin = io.a & io.cin
    io.cout @= a_and_b | b_and_cin | a_and_cin
