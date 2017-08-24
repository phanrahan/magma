from magma import wire, compile, EndCircuit
from loam.boards.icestick import IceStick, Counter

icestick = IceStick()
icestick.Clock.on()
icestick.D1.on()

main = icestick.main()

counter = Counter(24)
wire(counter.O[-1], main.D1)

EndCircuit()
