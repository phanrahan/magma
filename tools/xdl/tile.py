import sys
from magma.device import Device

fpga = 'xc3s250e.xdlrc'
if len(sys.argv) == 2:
    fpga = sys.argv[1]

device = Device(fpga)

print(fpga)
print('tiles %d %d' % (device.nx, device.ny))

print("  ", "".join(map(lambda x: ("%02d" % x)[-2:-1], range(device.nx))))
print("  ", "".join(map(lambda x: ("%02d" % x)[-1:],   range(device.nx))))

for y in range(device.ny):
    line = "%02d " % y

    for x in range(device.nx):
        tilesite = device.tiles[x][y]['tilename']

        if  tilesite.startswith("TI") \
         or tilesite.startswith("LI") \
         or tilesite.startswith("BI") \
         or tilesite.startswith("RI"):
            tilesite = "I"
        elif tilesite.startswith("CLK") or  tilesite.startswith("GCLK"):
            tilesite = "C"
        elif tilesite.startswith("DCM"):
            tilesite = "D"
        elif tilesite.startswith("CLB") \
          or tilesite.startswith("CLE"):
            tilesite = "S"
        elif tilesite.startswith("BRAM") or tilesite.startswith("EMPTY_BRAM"):
            tilesite = "B"
        elif tilesite.startswith("INT"):
            tilesite = "X"
        else:
            tilesite = "."

        #if tilesite != 'L': tilesite = '.'

        line += tilesite[0:1]

    print(line)

