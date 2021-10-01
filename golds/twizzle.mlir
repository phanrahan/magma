hw.module @twizzler(%I0: i1, %I1: i1, %I2: i1) -> (%O0: i1, %O1: i1, %O2: i1) {
    %0 = hw.constant -1 : i1
    %1 = hw.constant -1 : i1
    %2 = hw.constant -1 : i1
    %3 = comb.xor %I1, %0 : i1
    %4 = comb.xor %I0, %1 : i1
    %5 = comb.xor %I2, %2 : i1
    hw.output %3, %4, %5 : i1, i1, i1
}
hw.module @twizzle(%I: i1) -> (%O: i1) {
    %0 = sv.wire : !hw.inout<i1>
    %1 = sv.wire : !hw.inout<i1>
    %2 = sv.wire : !hw.inout<i1>
    %3 = sv.read_inout %0 : !hw.inout<i1>
    %4 = sv.read_inout %1 : !hw.inout<i1>
    %5 = sv.read_inout %2 : !hw.inout<i1>
    %7, %8, %6 = hw.instance "t1" @twizzler(%5, %4, %3) : (i1, i1, i1) -> (i1, i1, i1)
    %9, %10, %11 = hw.instance "t0" @twizzler(%I, %7, %8) : (i1, i1, i1) -> (i1, i1, i1)
    sv.assign %2, %9 : i1
    sv.assign %1, %10 : i1
    sv.assign %0, %11 : i1
    hw.output %6 : i1
}
