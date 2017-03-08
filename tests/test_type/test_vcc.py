from magma import *

def test():
    assert str(VCC) == "VCC"
    assert isinstance(VCC, BitOut)

    assert str(GND) == "GND"
    assert isinstance(GND, BitOut)

    assert VCC == VCC
    assert VCC != GND
    assert GND == GND
