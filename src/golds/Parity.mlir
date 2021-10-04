hw.module @Mux2x_SequentialRegisterWrapperBit(%I0: i1, %I1: i1, %S: i1) -> (%O: i1) {
    %0 = hw.array_create %I1, %I0 : i1
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi1>
    %5 = comb.extract %4 from 0 : (i1) -> i1
    hw.output %5 : i1
}
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
hw.module @Parity(%I: i1, %CLK: i1) -> (%O: i1) {
    %0 = hw.constant 0 : i1
    %1 = hw.constant 0 : i1
    %2 = hw.constant 1 : i1
    %3 = hw.constant 1 : i1
    %4 = hw.constant -1 : i1
    %5 = hw.constant -1 : i1
    %6 = sv.wire : !hw.inout<i1>
    %7 = sv.wire : !hw.inout<i1>
    %8 = sv.read_inout %6 : !hw.inout<i1>
    %9 = sv.read_inout %7 : !hw.inout<i1>
    %10 = comb.xor %8, %0 : i1
    %11 = comb.xor %10, %5 : i1
    %12 = hw.instance "Mux2xBit_inst0" @Mux2xBit(%1, %2, %11) : (i1, i1, i1) -> (i1)
    %13 = hw.instance "Mux2x_SequentialRegisterWrapperBit_inst0" @Mux2x_SequentialRegisterWrapperBit(%9, %12, %I) : (i1, i1, i1) -> (i1)
    %14 = hw.instance "Register_inst0" @Register(%13, %CLK) : (i1, i1) -> (i1)
    %15 = comb.xor %14, %3 : i1
    sv.assign %6, %14 : i1
    sv.assign %7, %14 : i1
    %16 = comb.xor %15, %4 : i1
    hw.output %16 : i1
}
