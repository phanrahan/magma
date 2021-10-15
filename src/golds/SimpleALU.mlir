hw.module @Mux2xUInt4(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
    %0 = hw.array_create %I1, %I0 : i4
    %1 = comb.merge %S : i1
    %2 = hw.struct_create (%0, %1) : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %4 = hw.struct_extract %2["data"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %5 = hw.struct_extract %2["sel"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %3 = hw.array_get %4[%5] : !hw.array<2xi4>
    hw.output %3 : i4
}
hw.module @SimpleALU(%a: i4, %b: i4, %opcode: i2) -> (%out: i4) {
    %0 = hw.constant 2 : i2
    %1 = comb.icmp eq %opcode, %0 : i2
    %2 = hw.instance "Mux2xUInt4_inst0" @Mux2xUInt4(%b, %a, %1) : (i4, i4, i1) -> (i4)
    %3 = comb.sub %a, %b : i4
    %4 = hw.constant 1 : i2
    %5 = comb.icmp eq %opcode, %4 : i2
    %6 = hw.instance "Mux2xUInt4_inst1" @Mux2xUInt4(%2, %3, %5) : (i4, i4, i1) -> (i4)
    %7 = comb.add %a, %b : i4
    %8 = hw.constant 0 : i2
    %9 = comb.icmp eq %opcode, %8 : i2
    %10 = hw.instance "Mux2xUInt4_inst2" @Mux2xUInt4(%6, %7, %9) : (i4, i4, i1) -> (i4)
    hw.output %10 : i4
}
