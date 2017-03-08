import sys
from magma.device import Device

fpga = 'xc3s250e.xdlrc'
if len(sys.argv) == 2:
    fpga = sys.argv[1]

device = Device(fpga)

print(device.fullname, device.family, device.device, device.package, device.speed)

prim = device.IOB
print(prim)
print("Output pins:", prim.outputs )
print("Input pins:", prim.inputs )

