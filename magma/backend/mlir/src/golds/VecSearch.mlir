hw.module @VecSearch(%CLK: i1) -> (out: i4) {
    %0 = hw.constant 0 : i4
    %1 = hw.constant 4 : i4
    %2 = hw.constant 15 : i4
    %3 = hw.constant 14 : i4
    %4 = hw.constant 2 : i4
    %5 = hw.constant 5 : i4
    %6 = hw.constant 13 : i4
    %7 = hw.constant 1 : i3
    %9 = comb.add %8, %7 : i3
    %10 = sv.reg {name = "Register_inst0"} : !hw.inout<i3>
    sv.alwaysff(posedge %CLK) {
        sv.passign %10, %9 : i3
    }
    %11 = hw.constant 0 : i3
    sv.initial {
        sv.bpassign %10, %11 : i3
    }
    %8 = sv.read_inout %10 : !hw.inout<i3>
    %13 = hw.array_create %0, %1, %2, %3, %4, %5, %6 : i4
    %12 = hw.array_get %13[%8] : !hw.array<7xi4>
    hw.output %12 : i4
}
