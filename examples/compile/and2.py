from magma import wire
from loam.boards.icestick import IceStick, And

icestick = IceStick()
for i in range(2):
    icestick.J1[i].input().on()
icestick.D5.on()

main = icestick.main()

and2 = And(2)
and2(main.J1[0], main.J1[1])
wire(and2.O, main.D5)

