import hwtypes as ht

from magma.bit import Bit
from magma.circuit import Circuit
from magma.clock import Clock
from magma.interface import IO
from magma.t import In, Out
from magma.generator import Generator2


def _filter_range(freq_in, divr, divf):
    pfd = freq_in / (divr + 1)
    vco = pfd * (divf + 1)

    if pfd < 17:
        return 1
    if pfd < 26:
        return 2
    if pfd < 44:
        return 3
    if pfd < 66:
        return 4
    if pfd < 101:
        return 5
    return 6


def _compute_params(freq_in, freq_out):
    freq_in /= 1000000
    freq_out /= 1000000

    best_freq_out = 0.
    for divr in range(16):
        pfd = freq_in / (divr + 1)
        if pfd < 10 or pfd > 133:
            continue

        for divf in range(64):
            vco = pfd * (divf + 1)
            if vco < 533 or vco > 1066:
                continue

            # The valid range for DIVQ is 1..6.
            #
            # This is correctly documented in the ICE Technology Library
            # Document, but unfortunately incorrectly documented as 0..7
            # in the iCE40 sysCLOCK PLL Design and Usage Guide.
            for divq in range(1, 7):
                fout = vco / (1 << divq)

                # simple mode
                if abs(fout - freq_out) < abs(best_freq_out - freq_out):
                    best_div_r = divr
                    best_div_f = divf
                    best_div_q = divq
                    best_freq_out = fout
    return (
        best_div_r,
        best_div_f,
        best_div_q,
        _filter_range(freq_in, best_div_r, best_div_f)
    )


def _make_pll_io():
    return IO(
        REFERENCECLK=In(Clock),
        RESETB=In(Bit),
        BYPASS=In(Bit),
        PLLOUTCORE=Out(Bit),
        PLLOUTGLOBAL=Out(Clock)
    )


class SB_PLL40_CORE(Circuit):
    io = _make_pll_io()

    param_types = {
        "FEEDBACK_PATH": str,
        "PLLOUT_SELECT": str,
        "DIVR": ht.BitVector[4],  # Reference clock divider (div+1) [0, ..., 15]
        "DIVF": ht.BitVector[7],  # Feedback divider (div+1) [0, ..., 63]
        "DIVQ": ht.BitVector[3],  # VCO divider (divq+1) [0, ..., 6]
        "FILTER_RANGE": ht.BitVector[3]
    }


class SB_PLL(Generator2):
    def __init__(self, freq_out, freq_in=12000000):
        """
        TODO(leonardt): This is a param wrapper, so shouldn't necessarily be a
        generator
        """
        self.name = "SB_PLL"
        self.io = _make_pll_io()

        divr, divf, divq, filter = _compute_params(freq_in, freq_out)

        pll = SB_PLL40_CORE(
            FEEDBACK_PATH="SIMPLE",
            PLLOUT_SELECT="GENCLK",
            DIVR=ht.BitVector[4](divr),
            DIVF=ht.BitVector[7](divf),
            DIVQ=ht.BitVector[3](divf),
            FILTER_RANGE=ht.BitVector[3](filter)
        )

        pll.REFERENCECLK @= self.io.REFERENCECLK
        pll.RESETB @= self.io.RESETB
        pll.BYPASS @= self.io.BYPASS
        self.io.PLLOUTCORE @= pll.PLLOUTCORE
        self.io.PLLOUTGLOBAL @= pll.PLLOUTGLOBAL
