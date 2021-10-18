hw.module @Register(%I: i16, %CLK: i1) -> (%O: i16) {
    %1 = sv.reg {name = "reg_P16_inst0"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %I : i16
    }
    %2 = hw.constant 0 : i16
    sv.initial {
        sv.bpassign %1, %2 : i16
    }
    %0 = sv.read_inout %1 : !hw.inout<i16>
    hw.output %0 : i16
}
hw.module @GCD(%a: i16, %b: i16, %load: i1, %CLK: i1) -> (%O0: i16, %O1: i1) {
    %2 = comb.sub %0, %1 : i16
    %3 = comb.icmp ult %0, %1 : i16
    %5 = hw.array_create %2, %0 : i16
    %4 = hw.array_get %5[%3] : !hw.array<2xi16>
    %6 = hw.constant 0 : i16
    %7 = comb.icmp eq %0, %6 : i16
    %9 = hw.constant -1 : i1
    %8 = comb.xor %9, %7 : i1
    %11 = hw.array_create %0, %4 : i16
    %10 = hw.array_get %11[%8] : !hw.array<2xi16>
    %13 = hw.array_create %10, %b : i16
    %12 = hw.array_get %13[%load] : !hw.array<2xi16>
    %0 = hw.instance "Register_inst1" @Register(%12, %CLK) : (i16, i1) -> (i16)
    %14 = comb.sub %1, %0 : i16
    %16 = hw.array_create %1, %14 : i16
    %15 = hw.array_get %16[%3] : !hw.array<2xi16>
    %18 = hw.array_create %1, %15 : i16
    %17 = hw.array_get %18[%8] : !hw.array<2xi16>
    %20 = hw.array_create %17, %a : i16
    %19 = hw.array_get %20[%load] : !hw.array<2xi16>
    %1 = hw.instance "Register_inst0" @Register(%19, %CLK) : (i16, i1) -> (i16)
    %21 = hw.constant 0 : i16
    %22 = comb.icmp eq %0, %21 : i16
    hw.output %1, %22 : i16, i1
}
