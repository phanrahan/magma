from magma import wire, compile, EndCircuit
from loam.boards.icestick import IceStick, Counter
from pipeline import Pipeline


icestick = IceStick()
icestick.Clock.on()
icestick.D1.on()
icestick.D2.on()
icestick.D3.on()
icestick.D4.on()
icestick.D5.on()

main = icestick.main()

# decrease the frequency to avoid timing violation
counter = Counter(4)
pipeline = Pipeline()
wire(counter.O[-1], pipeline.CLK)
wire(pipeline.O[:4], [main.D1, main.D2, main.D3, main.D4])
# light 5 indicates the end of prediction
wire(pipeline.D, main.D5)

EndCircuit()