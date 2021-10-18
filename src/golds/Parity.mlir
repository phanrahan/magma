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
hw.module @Parity(%I: i1, %CLK: i1) -> (%O: i1) {
    %0 = hw.constant 0 : i1
    %1 = hw.constant 1 : i1
    %2 = hw.constant 0 : i1
    %4 = comb.xor %3, %2 : i1
    %6 = hw.constant -1 : i1
    %5 = comb.xor %6, %4 : i1
    %8 = hw.array_create %0, %1 : i1
    %7 = hw.array_get %8[%5] : i2
    %10 = hw.array_create %3, %7 : i1
    %9 = hw.array_get %10[%I] : i2
    %3 = hw.instance "Register_inst0" @Register(%9, %CLK) : (i1, i1) -> (i1)
    %11 = hw.constant 1 : i1
    %12 = comb.xor %3, %11 : i1
    %14 = hw.constant -1 : i1
    %13 = comb.xor %14, %12 : i1
    hw.output %13 : i1
}
