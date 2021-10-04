hw.module @Mux2xUInt4(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
    %0 = hw.array_create %I1, %I0 : i4
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi4>
    hw.output %4 : i4
}
hw.module @BasicALU(%a: i4, %b: i4, %opcode: i4) -> (%out: i4) {
    %0 = hw.constant 0 : i4
    %1 = hw.constant 1 : i4
    %2 = hw.constant 2 : i4
    %3 = hw.constant 1 : i4
    %4 = hw.constant 3 : i4
    %5 = hw.constant 1 : i4
    %6 = hw.constant 4 : i4
    %7 = hw.constant 4 : i4
    %8 = hw.constant 5 : i4
    %9 = hw.constant 4 : i4
    %10 = hw.constant 6 : i4
    %11 = hw.constant 7 : i4
    %12 = hw.constant 8 : i4
    %13 = hw.constant 0 : i1
    %14 = hw.constant 0 : i1
    %15 = hw.constant 0 : i1
    %16 = hw.constant 0 : i1
    %17 = hw.constant 0 : i1
    %18 = hw.constant 0 : i1
    %19 = comb.add %a, %b : i4
    %20 = comb.sub %a, %b : i4
    %21 = comb.icmp ult %a, %b : i4
    %22 = comb.icmp eq %a, %b : i4
    %23 = comb.icmp eq %opcode, %0 : i4
    %24 = comb.icmp eq %opcode, %1 : i4
    %25 = comb.icmp eq %opcode, %2 : i4
    %26 = comb.add %a, %3 : i4
    %27 = comb.icmp eq %opcode, %4 : i4
    %28 = comb.sub %a, %5 : i4
    %29 = comb.icmp eq %opcode, %6 : i4
    %30 = comb.add %a, %7 : i4
    %31 = comb.icmp eq %opcode, %8 : i4
    %32 = comb.sub %a, %9 : i4
    %33 = comb.icmp eq %opcode, %10 : i4
    %34 = comb.icmp eq %opcode, %11 : i4
    %35 = comb.icmp eq %opcode, %12 : i4
    %36 = comb.concat %18, %17, %16, %21 : (i1, i1, i1, i1) -> i4
    %37 = comb.concat %15, %14, %13, %22 : (i1, i1, i1, i1) -> i4
    %38 = hw.instance "Mux2xUInt4_inst0" @Mux2xUInt4(%37, %36, %35) : (i4, i4, i1) -> (i4)
    %39 = hw.instance "Mux2xUInt4_inst1" @Mux2xUInt4(%38, %20, %34) : (i4, i4, i1) -> (i4)
    %40 = hw.instance "Mux2xUInt4_inst2" @Mux2xUInt4(%39, %19, %33) : (i4, i4, i1) -> (i4)
    %41 = hw.instance "Mux2xUInt4_inst3" @Mux2xUInt4(%40, %32, %31) : (i4, i4, i1) -> (i4)
    %42 = hw.instance "Mux2xUInt4_inst4" @Mux2xUInt4(%41, %30, %29) : (i4, i4, i1) -> (i4)
    %43 = hw.instance "Mux2xUInt4_inst5" @Mux2xUInt4(%42, %28, %27) : (i4, i4, i1) -> (i4)
    %44 = hw.instance "Mux2xUInt4_inst6" @Mux2xUInt4(%43, %26, %25) : (i4, i4, i1) -> (i4)
    %45 = hw.instance "Mux2xUInt4_inst7" @Mux2xUInt4(%44, %b, %24) : (i4, i4, i1) -> (i4)
    %46 = hw.instance "Mux2xUInt4_inst8" @Mux2xUInt4(%45, %a, %23) : (i4, i4, i1) -> (i4)
    hw.output %46 : i4
}
