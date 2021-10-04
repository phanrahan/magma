hw.module @Register(%I: i1, %CLK: i1) -> (%O: i1) {
    %0 = sv.reg {name = "reg_P1_inst0"} : !hw.inout<i1>
    %1 = hw.constant 0 : i1
    %2 = sv.read_inout %0 : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) { sv.passign %0, %I : i1 }
    sv.initial { sv.bpassign %0, %1 : i1 }
    %3 = comb.extract %2 from 0 : (i1) -> i1
    hw.output %3 : i1
}
hw.module @Mux2xBit(%I0: i1, %I1: i1, %S: i1) -> (%O: i1) {
    %0 = hw.array_create %I1, %I0 : i1
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi1>
    %5 = comb.extract %4 from 0 : (i1) -> i1
    hw.output %5 : i1
}
hw.module @Cell(%neighbors: i8, %running: i1, %write_enable: i1, %write_value: i1, %CLK: i1) -> (%out: i1) {
    %0 = hw.constant 0 : i3
    %1 = hw.constant 0 : i1
    %2 = hw.constant 0 : i1
    %3 = hw.constant 0 : i1
    %4 = hw.constant 0 : i1
    %5 = hw.constant 0 : i1
    %6 = hw.constant 0 : i1
    %7 = hw.constant 0 : i1
    %8 = hw.constant 0 : i1
    %9 = hw.constant 0 : i1
    %10 = hw.constant 0 : i1
    %11 = hw.constant 0 : i1
    %12 = hw.constant 0 : i1
    %13 = hw.constant 0 : i1
    %14 = hw.constant 0 : i1
    %15 = hw.constant 0 : i1
    %16 = hw.constant 0 : i1
    %17 = hw.constant 2 : i3
    %18 = hw.constant 4 : i3
    %19 = hw.constant 0 : i1
    %20 = hw.constant 1 : i1
    %21 = hw.constant 0 : i1
    %22 = hw.constant 3 : i3
    %23 = hw.constant 0 : i1
    %24 = hw.constant 1 : i1
    %25 = hw.constant -1 : i1
    %26 = hw.constant -1 : i1
    %27 = sv.wire : !hw.inout<i1>
    %28 = sv.wire : !hw.inout<i1>
    %29 = comb.extract %neighbors from 0 : (i8) -> i1
    %30 = comb.extract %neighbors from 1 : (i8) -> i1
    %31 = comb.extract %neighbors from 2 : (i8) -> i1
    %32 = comb.extract %neighbors from 3 : (i8) -> i1
    %33 = comb.extract %neighbors from 4 : (i8) -> i1
    %34 = comb.extract %neighbors from 5 : (i8) -> i1
    %35 = comb.extract %neighbors from 6 : (i8) -> i1
    %36 = comb.extract %neighbors from 7 : (i8) -> i1
    %37 = comb.xor %running, %25 : i1
    %38 = sv.read_inout %27 : !hw.inout<i1>
    %39 = sv.read_inout %28 : !hw.inout<i1>
    %40 = comb.concat %2, %1, %29 : (i1, i1, i1) -> i3
    %41 = comb.concat %4, %3, %30 : (i1, i1, i1) -> i3
    %42 = comb.concat %6, %5, %31 : (i1, i1, i1) -> i3
    %43 = comb.concat %8, %7, %32 : (i1, i1, i1) -> i3
    %44 = comb.concat %10, %9, %33 : (i1, i1, i1) -> i3
    %45 = comb.concat %12, %11, %34 : (i1, i1, i1) -> i3
    %46 = comb.concat %14, %13, %35 : (i1, i1, i1) -> i3
    %47 = comb.concat %16, %15, %36 : (i1, i1, i1) -> i3
    %48 = comb.xor %38, %26 : i1
    %49 = hw.instance "Register_inst0" @Register(%39, %CLK) : (i1, i1) -> (i1)
    %50 = comb.add %0, %40 : i3
    %51 = hw.instance "Mux2xBit_inst0" @Mux2xBit(%49, %write_value, %write_enable) : (i1, i1, i1) -> (i1)
    sv.assign %27, %49 : i1
    %52 = comb.add %50, %41 : i3
    %53 = comb.add %52, %42 : i3
    %54 = comb.add %53, %43 : i3
    %55 = comb.add %54, %44 : i3
    %56 = comb.add %55, %45 : i3
    %57 = comb.add %56, %46 : i3
    %58 = comb.add %57, %47 : i3
    %59 = comb.icmp ult %58, %17 : i3
    %60 = comb.icmp ult %58, %18 : i3
    %61 = comb.icmp eq %58, %22 : i3
    %62 = hw.instance "Mux2xBit_inst1" @Mux2xBit(%19, %20, %60) : (i1, i1, i1) -> (i1)
    %63 = comb.and %48, %61 : i1
    %64 = hw.instance "Mux2xBit_inst2" @Mux2xBit(%62, %21, %59) : (i1, i1, i1) -> (i1)
    %65 = hw.instance "Mux2xBit_inst3" @Mux2xBit(%23, %24, %63) : (i1, i1, i1) -> (i1)
    %66 = hw.instance "Mux2xBit_inst4" @Mux2xBit(%65, %64, %49) : (i1, i1, i1) -> (i1)
    %67 = hw.instance "Mux2xBit_inst5" @Mux2xBit(%66, %51, %37) : (i1, i1, i1) -> (i1)
    sv.assign %28, %67 : i1
    hw.output %49 : i1
}
