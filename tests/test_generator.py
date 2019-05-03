import magma as m


class IO:
    def __init__(self, **kwargs):
        self.interface = {}
        for k, v in kwargs.items():
            port = v.flip()()
            self.interface[k] = type(port)
            setattr(self, k, port)

    def __repr__(self):
        return repr(self.interface)


class PassThroughGen(m.GeneratorBase):
    def __new__(cls, width):
        io = IO(I=m.In(m.Bits[width]), O=m.Out(m.Bits[width]))
        m.wire(io.I, io.O)
        return io


"""
class NewGen(m.GeneratorBase):
    width : int

    width * 2

    def generate(params):
        io = IO(I=m.In(m.Bits[width]), O=m.Out(m.Bits[width]))
"""


def test_new_generator():
    metacls = PassThroughGen
    cls = metacls(8)
    inst = cls()
    assert type(inst) == cls
    assert type(cls) == metacls

main_test = test_new_generator

if __name__ == "__main__":
    main_test()
