import re, sys
from magma.device import Device

fpga = 'xc3s250e.xdlrc'
if len(sys.argv) == 2:
    fpga = sys.argv[1]

device = Device(fpga)

print(device.fullname, device.family, device.device, device.package, device.speed)


minx = 1000
maxx = 0
miny = 1000
maxy = 0
n = 0
for k, v in device.sites.items():
    if k.startswith('SLICE'):
        m = re.search(r'SLICE_X(\d*)Y(\d*)', k)
	if m:
	    x = int(m.group(1))
	    y = int(m.group(2))
	    if x < minx: minx = x
	    if x > maxx: maxx = x
	    if y < miny: miny = y
	    if y > maxy: maxy = y
	    #print(m.groups())
	    #print(x, y)
	n += 1

print(n, 'slices')
print('x:', minx, maxx, 'y:', miny, maxy)

print("  ", "".join(map(lambda x: ("%02d" % x)[-2:-1], range(minx, maxx+1))))
print("  ", "".join(map(lambda x: ("%02d" % x)[-1:],   range(minx, maxx+1))))

for yy in range(miny, maxy+1):
    y = maxy - yy
    line = "%02d " % y
    for x in range(minx, maxx+1):
        if 'SLICE_X%dY%d' % (x,y) in device.sites:
            line += 'S'
        else:
            line += '.'
    print(line)
        



