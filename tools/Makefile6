# Makefile to compile and download a simple Verilog program

DEVICE=XC6SLX9
SPEED=2
PACKAGE=TQG144
PART=${DEVICE}-${SPEED}-${PACKAGE}

TARGET=main
SRC=main.v 

default: ${TARGET}.bit

${TARGET}.prj: ${SRC}
	rm -fr ${TARGET}.prj
	for f in ${SRC}; do \
	    echo "verilog work $$f" >> ${TARGET}.prj ;\
	done 

${TARGET}.ngc: ${TARGET}.prj
	@echo 'run'                 > xst.cmd
	@echo '-ifn $(TARGET).prj' >> xst.cmd
	@echo '-ifmt mixed'        >> xst.cmd
	@echo '-top main'          >> xst.cmd
	@echo '-ofn $(TARGET).ngc' >> xst.cmd
	@echo '-ofmt NGC' 	   >> xst.cmd
	@echo '-p $(PART)'         >> xst.cmd
	@echo '-opt_mode Speed'	   >> xst.cmd
	@echo '-opt_level 1'	   >> xst.cmd
	xst -ifn xst.cmd

${TARGET}.ngd: ${TARGET}.ngc ${TARGET}.ucf
	ngdbuild -p $(PART) -uc ${TARGET}.ucf ${TARGET}.ngc

${TARGET}.ncd: ${TARGET}.ngd
	map -w -detail -pr b ${TARGET}.ngd

${TARGET}.pcf: ${TARGET}.ngd
	map -w -detail -pr b ${TARGET}.ngd

parout.ncd: ${TARGET}.ncd
	par -w ${TARGET}.ncd parout.ncd ${TARGET}.pcf
	xdl -ncd2xdl parout.ncd parout.xdl

${TARGET}.bit: parout.ncd
	bitgen -w -g CRC:Enable -g StartUpClk:CClk \
   	  parout.ncd ${TARGET}.bit ${TARGET}.pcf

upload: 
	papilio-prog -v -f ${TARGET}.bit -b ../bscan_spi_lx9_qfp144.bit -sa -r
	papilio-prog -c

clean: cruft 
	rm -rf \
	${TARGET}.prj \
	${TARGET}.ngc \
	${TARGET}.ngd \
	${TARGET}.ncd ${TARGET}.pcf \
	parout.ncd \
	${TARGET}.bit 

cruft:
	rm -rf \
	${TARGET}.lso  ${TARGET}.ngc_xst.xrpt xst.srp xst.rpt xst xst.cmd \
	${TARGET}.bld ${TARGET}_ngdbuild.xrpt netlist.lst \
	xlnx_auto_0.ise xlnx_auto_0_xdb \
	${TARGET}.map ${TARGET}.mrp ${TARGET}.ngm \
	${TARGET}_map.xrpt ${TARGET}_summary.xml ${TARGET}_usage.xml \
	parout_pad.txt parout.pad parout_pad.csv \
	parout.xpi parout.par parout.ptwx parout.unroutes \
	par_usage_statistics.html \
	${TARGET}_par.xrpt \
        ${TARGET}.bgn ${TARGET}.bin ${TARGET}.drc ${TARGET}.prm \
	${TARGET}_bitgen.xwbt usage_statistics_webtalk.html  webtalk.log \
	_xmsgs


