import magma as m
import fault


def test_channel():
    @m.circuit.coroutine
    def downsample(data_in: m.In(m.Channel(m.Bits[16])),
                   data_out: m.Out(m.Channel(m.Bits[16]))):
        while True:
            for y in range(32):
                for x in range(32):
                    data = data_in.pop()
                    if ((x % m.bits(2, 5)) == 0) & ((y % m.bits(2, 5)) == 0):
                        data_out.push(data)
                    yield

    m.compile("build/downsample", downsample, output="coreir-verilog")
    tester = fault.Tester(downsample, downsample.CLK)
    for data in [0xDEAD, 0xBEEF]:
        tester.poke(downsample.data_in, 0xDE)
        tester.poke(downsample.data_in_valid, 1)
        tester.eval()
        tester.print("data_out=%x data_out_valid=%d", downsample.O0, downsample.O1)
    tester.compile_and_run("verilator", directory="tests/build", skip_compile=True)
