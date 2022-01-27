hw.module @GCD(%a: i16, %b: i16, %load: i1, %CLK: i1) -> (O0: i16, O1: i1) {
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
    %14 = sv.reg {name = "Register_inst1"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %14, %12 : i16
    }
    %15 = hw.constant 0 : i16
    sv.initial {
        sv.bpassign %14, %15 : i16
    }
    %0 = sv.read_inout %14 : !hw.inout<i16>
    %16 = comb.sub %1, %0 : i16
    %18 = hw.array_create %1, %16 : i16
    %17 = hw.array_get %18[%3] : !hw.array<2xi16>
    %20 = hw.array_create %1, %17 : i16
    %19 = hw.array_get %20[%8] : !hw.array<2xi16>
    %22 = hw.array_create %19, %a : i16
    %21 = hw.array_get %22[%load] : !hw.array<2xi16>
    %23 = sv.reg {name = "Register_inst0"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %23, %21 : i16
    }
    sv.initial {
        sv.bpassign %23, %15 : i16
    }
    %1 = sv.read_inout %23 : !hw.inout<i16>
    %24 = hw.constant 0 : i16
    %25 = comb.icmp eq %0, %24 : i16
    hw.output %1, %25 : i16, i1
}
