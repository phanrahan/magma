def test_545():
    import magma
    @magma.circuit.sequential
    class PE:
        def __call__(self, in0 : magma.Bit, in1: magma.Bit) -> magma.Bit:
            return in0 & in1
