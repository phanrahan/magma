hw.module @Mux2x_SequentialRegisterWrapperBit(%I0: i1, %I1: i1, %S: i1) -> (%O: i1) {
    %0 = comb.merge %I0 : i1
    %1 = comb.merge %I1 : i1
    %2 = hw.array_create %1, %0 : i1
    %3 = comb.merge %S : i1
    %4 = hw.struct_create (%2, %3) : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %6 = hw.struct_extract %4["data"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %7 = hw.struct_extract %4["sel"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %5 = hw.array_get %6[%7] : !hw.array<2xi1>
    %8 = comb.extract %5 from 0 : (i1) -> i1
    hw.output %8 : i1
}
hw.module @Register(%I: i1, %CLK: i1) -> (%O: i1) {
    %0 = comb.merge %I : i1
    %2 = sv.reg {name = "reg_P1_inst0"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %2, %0 : i1
    }
    %3 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %2, %3 : i1
    }
    %1 = sv.read_inout %2 : !hw.inout<i1>
    %4 = comb.extract %1 from 0 : (i1) -> i1
    hw.output %4 : i1
}
hw.module @Mux2xBit(%I0: i1, %I1: i1, %S: i1) -> (%O: i1) {
    %0 = comb.merge %I0 : i1
    %1 = comb.merge %I1 : i1
    %2 = hw.array_create %1, %0 : i1
    %3 = comb.merge %S : i1
    %4 = hw.struct_create (%2, %3) : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %6 = hw.struct_extract %4["data"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %7 = hw.struct_extract %4["sel"] : !hw.struct<data: !hw.array<2xi1>, sel: i1>
    %5 = hw.array_get %6[%7] : !hw.array<2xi1>
    %8 = comb.extract %5 from 0 : (i1) -> i1
    hw.output %8 : i1
}
hw.module @Parity(%I: i1, %CLK: i1) -> (%O: i1) {
    %0 = hw.constant 0 : i1
    %1 = hw.constant 1 : i1
    %2 = hw.constant 0 : i1
    %4 = comb.xor %3, %2 : i1
    %6 = hw.constant -1 : i1
    %5 = comb.xor %6, %4 : i1
    %7 = hw.instance "Mux2xBit_inst0" @Mux2xBit(%0, %1, %5) : (i1, i1, i1) -> (i1)
    %8 = hw.instance "Mux2x_SequentialRegisterWrapperBit_inst0" @Mux2x_SequentialRegisterWrapperBit(%3, %7, %I) : (i1, i1, i1) -> (i1)
    %3 = hw.instance "Register_inst0" @Register(%8, %CLK) : (i1, i1) -> (i1)
    %9 = hw.constant 1 : i1
    %10 = comb.xor %3, %9 : i1
    %12 = hw.constant -1 : i1
    %11 = comb.xor %12, %10 : i1
    hw.output %11 : i1
}
