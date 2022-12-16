import pygal
import timeit
import magma as m


def gen_circuit(debug_mode, n=8):
    if debug_mode == 2:
        m.config.config.use_generator_debug_rewriter = True
    else:
        m.config.config.use_generator_debug_rewriter = False

    class Foo(m.Generator2):
        if debug_mode == 2:
            def __init__(self, n):
                self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bit))
                x = m.Bits[n]()
                x @= ~self.io.I
                self.io.O @= x.reduce_xor()
        elif debug_mode == 1:
            def __init__(self, n):
                m.config.set_debug_mode(True)
                self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bit))
                x = m.Bits[n]()
                x @= ~self.io.I
                self.io.O @= x.reduce_xor()
                m.config.set_debug_mode(False)
        else:
            def __init__(self, n):
                self.io = m.IO(I=m.In(m.Bits[n]), O=m.Out(m.Bit))
                x = m.Bits[n]()
                x @= ~self.io.I
                self.io.O @= x.reduce_xor()
    Foo(n)


data = {}

for debug_mode in [0, 1, 2]:
    data[debug_mode] = timeit.Timer(lambda:
                                    gen_circuit(debug_mode)).timeit(number=10)

bar = pygal.Bar()
bar.add('Off', data[0])
bar.add('Old', data[1])
bar.add('New', data[2])
bar.render_to_file("debug.svg")
