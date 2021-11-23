hw.module @Parity(%I: i1, %CLK: i1) -> (O: i1) {
    %0 = hw.constant 0 : i1
    %1 = hw.constant 1 : i1
    %2 = hw.constant 0 : i1
    %4 = comb.xor %3, %2 : i1
    %6 = hw.constant -1 : i1
    %5 = comb.xor %6, %4 : i1
    %8 = hw.array_create %0, %1 : i1
    %7 = hw.array_get %8[%5] : !hw.array<2xi1>
    %10 = hw.array_create %3, %7 : i1
    %9 = hw.array_get %10[%I] : !hw.array<2xi1>
    %11 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %11, %9 : i1
    }
    %12 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %11, %12 : i1
    }
    %3 = sv.read_inout %11 : !hw.inout<i1>
    %13 = hw.constant 1 : i1
    %14 = comb.xor %3, %13 : i1
    %15 = comb.xor %6, %14 : i1
    hw.output %15 : i1
}
