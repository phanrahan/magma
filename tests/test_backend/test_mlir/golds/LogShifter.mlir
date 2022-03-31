hw.module @LogShifter(%I: i16, %shift_amount: i4, %CLK: i1) -> (O: i16) {
    %0 = hw.constant 8 : i16
    %1 = comb.shl %I, %0 : i16
    %2 = comb.extract %shift_amount from 3 : (i4) -> i1
    %3 = hw.constant 1 : i1
    %4 = comb.xor %2, %3 : i1
    %6 = hw.constant -1 : i1
    %5 = comb.xor %6, %4 : i1
    %8 = hw.array_create %I, %1 : i16
    %7 = hw.array_get %8[%5] : !hw.array<2xi16>
    %10 = sv.reg {name = "Register_inst0"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %10, %7 : i16
    }
    %11 = hw.constant 0 : i16
    sv.initial {
        sv.bpassign %10, %11 : i16
    }
    %9 = sv.read_inout %10 : !hw.inout<i16>
    %12 = hw.constant 4 : i16
    %13 = comb.shl %9, %12 : i16
    %14 = comb.extract %shift_amount from 2 : (i4) -> i1
    %15 = hw.constant 1 : i1
    %16 = comb.xor %14, %15 : i1
    %17 = comb.xor %6, %16 : i1
    %19 = hw.array_create %9, %13 : i16
    %18 = hw.array_get %19[%17] : !hw.array<2xi16>
    %21 = sv.reg {name = "Register_inst1"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %21, %18 : i16
    }
    sv.initial {
        sv.bpassign %21, %11 : i16
    }
    %20 = sv.read_inout %21 : !hw.inout<i16>
    %22 = hw.constant 2 : i16
    %23 = comb.shl %20, %22 : i16
    %24 = comb.extract %shift_amount from 1 : (i4) -> i1
    %25 = hw.constant 1 : i1
    %26 = comb.xor %24, %25 : i1
    %27 = comb.xor %6, %26 : i1
    %29 = hw.array_create %20, %23 : i16
    %28 = hw.array_get %29[%27] : !hw.array<2xi16>
    %31 = sv.reg {name = "Register_inst2"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %31, %28 : i16
    }
    sv.initial {
        sv.bpassign %31, %11 : i16
    }
    %30 = sv.read_inout %31 : !hw.inout<i16>
    %32 = hw.constant 1 : i16
    %33 = comb.shl %30, %32 : i16
    %34 = comb.extract %shift_amount from 0 : (i4) -> i1
    %35 = hw.constant 1 : i1
    %36 = comb.xor %34, %35 : i1
    %37 = comb.xor %6, %36 : i1
    %39 = hw.array_create %30, %33 : i16
    %38 = hw.array_get %39[%37] : !hw.array<2xi16>
    hw.output %38 : i16
}
