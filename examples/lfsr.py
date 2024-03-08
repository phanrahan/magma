import os
import csv
import magma as m


def read_taps_table():
    """
    From Xilinx
    https://docs.xilinx.com/v/u/en-US/xapp052
    """
    taps_file = os.path.join(os.path.dirname(__file__), 'lfsr.csv')
    taps_table = {}
    with open(taps_file, 'r') as f:
        rows = csv.reader(f)
        assert next(rows) == ["BITS", "TAPS"]
        for row in rows:
            taps_table[int(row[0])] = [int(x) for x in row[1].split(",")]
    return taps_table


class LFSR(m.Generator):
    taps_table = read_taps_table()

    def __init__(self, n, init=None):
        if init is None:
            init = [0 for _ in range(n)]
        self.io = m.IO(O=m.Out(m.Bits[n])) + m.ClockIO()
        sipo = m.scan(
            (m.Register(m.Bit, init=bool(init[i]))() for i in range(n)),
            scanargs={"I": "O"}
        )

        taps = self.taps_table[n]
        self.io.O @= sipo(
            m.bits([sipo.O[tap - 1] for tap in taps]).reduce_xor()
        )
