hw.module @Mux2xUInt4(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
    %0 = hw.array_create %I1, %I0 : i4
    %1 = comb.merge %S : i1
    %2 = hw.struct_create (%0, %1) : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %4 = hw.struct_extract %2["data"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %5 = hw.struct_extract %2["sel"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %3 = hw.array_get %4[%5] : !hw.array<2xi4>
    hw.output %3 : i4
}
hw.module @BasicALU(%a: i4, %b: i4, %opcode: i4) -> (%out: i4) {
    %0 = comb.icmp eq %a, %b : i4
    %1 = hw.constant 0 : i1
    %2 = hw.constant 0 : i1
    %3 = hw.constant 0 : i1
    %4 = comb.concat %3, %2, %1, %0 : (i1, i1, i1, i1) -> (i4)
    %5 = comb.icmp ult %a, %b : i4
    %6 = hw.constant 0 : i1
    %7 = hw.constant 0 : i1
    %8 = hw.constant 0 : i1
    %9 = comb.concat %8, %7, %6, %5 : (i1, i1, i1, i1) -> (i4)
    %10 = hw.constant 8 : i4
    %11 = comb.icmp eq %opcode, %10 : i4
    %12 = hw.instance "Mux2xUInt4_inst0" @Mux2xUInt4(%4, %9, %11) : (i4, i4, i1) -> (i4)
    %13 = comb.sub %a, %b : i4
    %14 = hw.constant 7 : i4
    %15 = comb.icmp eq %opcode, %14 : i4
    %16 = hw.instance "Mux2xUInt4_inst1" @Mux2xUInt4(%12, %13, %15) : (i4, i4, i1) -> (i4)
    %17 = comb.add %a, %b : i4
    %18 = hw.constant 6 : i4
    %19 = comb.icmp eq %opcode, %18 : i4
    %20 = hw.instance "Mux2xUInt4_inst2" @Mux2xUInt4(%16, %17, %19) : (i4, i4, i1) -> (i4)
    %21 = hw.constant 4 : i4
    %22 = comb.sub %a, %21 : i4
    %23 = hw.constant 5 : i4
    %24 = comb.icmp eq %opcode, %23 : i4
    %25 = hw.instance "Mux2xUInt4_inst3" @Mux2xUInt4(%20, %22, %24) : (i4, i4, i1) -> (i4)
    %26 = hw.constant 4 : i4
    %27 = comb.add %a, %26 : i4
    %28 = hw.constant 4 : i4
    %29 = comb.icmp eq %opcode, %28 : i4
    %30 = hw.instance "Mux2xUInt4_inst4" @Mux2xUInt4(%25, %27, %29) : (i4, i4, i1) -> (i4)
    %31 = hw.constant 1 : i4
    %32 = comb.sub %a, %31 : i4
    %33 = hw.constant 3 : i4
    %34 = comb.icmp eq %opcode, %33 : i4
    %35 = hw.instance "Mux2xUInt4_inst5" @Mux2xUInt4(%30, %32, %34) : (i4, i4, i1) -> (i4)
    %36 = hw.constant 1 : i4
    %37 = comb.add %a, %36 : i4
    %38 = hw.constant 2 : i4
    %39 = comb.icmp eq %opcode, %38 : i4
    %40 = hw.instance "Mux2xUInt4_inst6" @Mux2xUInt4(%35, %37, %39) : (i4, i4, i1) -> (i4)
    %41 = hw.constant 1 : i4
    %42 = comb.icmp eq %opcode, %41 : i4
    %43 = hw.instance "Mux2xUInt4_inst7" @Mux2xUInt4(%40, %b, %42) : (i4, i4, i1) -> (i4)
    %44 = hw.constant 0 : i4
    %45 = comb.icmp eq %opcode, %44 : i4
    %46 = hw.instance "Mux2xUInt4_inst8" @Mux2xUInt4(%43, %a, %45) : (i4, i4, i1) -> (i4)
    hw.output %46 : i4
}
