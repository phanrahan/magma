hw.module @Mux2xUInt4(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
    %0 = hw.array_create %I1, %I0 : i4
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi4>
    hw.output %4 : i4
}
hw.module @SimpleALU(%a: i4, %b: i4, %opcode: i2) -> (%out: i4) {
    %0 = hw.constant 0 : i2
    %1 = hw.constant 1 : i2
    %2 = hw.constant 2 : i2
    %3 = comb.add %a, %b : i4
    %4 = comb.sub %a, %b : i4
    %5 = comb.icmp eq %opcode, %0 : i2
    %6 = comb.icmp eq %opcode, %1 : i2
    %7 = comb.icmp eq %opcode, %2 : i2
    %8 = hw.instance "Mux2xUInt4_inst0" @Mux2xUInt4(%b, %a, %7) : (i4, i4, i1) -> (i4)
    %9 = hw.instance "Mux2xUInt4_inst1" @Mux2xUInt4(%8, %4, %6) : (i4, i4, i1) -> (i4)
    %10 = hw.instance "Mux2xUInt4_inst2" @Mux2xUInt4(%9, %3, %5) : (i4, i4, i1) -> (i4)
    hw.output %10 : i4
}
