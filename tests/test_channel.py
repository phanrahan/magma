import magma as m


def test_channel():
    @m.circuit.coroutine
    def downsample(data_in: m.In(m.Channel(m.Bits[16])),
                   data_out: m.Out(m.Channel(m.Bits[16]))):
        while True:
            for y in range(32):
                for x in range(32):
                    data = data_in.pop()
                    if (x % 2) & (y % 2):
                        data_out.push(data)
                    yield

    m.compile("test_downsample", downsample)
