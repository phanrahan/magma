import re, sys
from magma.device import Device

fpga = 'xc3s250e.xdlrc'
if len(sys.argv) == 2:
    fpga = sys.argv[1]

device = Device(fpga)

for y in range(device.ny):
    for x in range(device.nx):
        primsites = device.tiles[x][y]['sitenames']
	for i in range(len(primsites)):
	    p = primsites[i]
	    #print(p)
	    m = re.search(r'P(\d+)', p)
	    if m:
	    	print('Pin', m.group(1), 'on tile (%d, %d)' % (x,y))

