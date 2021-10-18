hw.module @LogShifter(%I: i16, %shift_amount: i4, %CLK: i1) -> (%O: i16) {
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
    %18 = hw.constant -1 : i1
    %17 = comb.xor %18, %16 : i1
    %20 = hw.array_create %9, %13 : i16
    %19 = hw.array_get %20[%17] : !hw.array<2xi16>
    %22 = sv.reg {name = "Register_inst1"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %22, %19 : i16
    }
    %23 = hw.constant 0 : i16
    sv.initial {
        sv.bpassign %22, %23 : i16
    }
    %21 = sv.read_inout %22 : !hw.inout<i16>
    %24 = hw.constant 2 : i16
    %25 = comb.shl %21, %24 : i16
    %26 = comb.extract %shift_amount from 1 : (i4) -> i1
    %27 = hw.constant 1 : i1
    %28 = comb.xor %26, %27 : i1
    %30 = hw.constant -1 : i1
    %29 = comb.xor %30, %28 : i1
    %32 = hw.array_create %21, %25 : i16
    %31 = hw.array_get %32[%29] : !hw.array<2xi16>
    %34 = sv.reg {name = "Register_inst2"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %34, %31 : i16
    }
    %35 = hw.constant 0 : i16
    sv.initial {
        sv.bpassign %34, %35 : i16
    }
    %33 = sv.read_inout %34 : !hw.inout<i16>
    %36 = hw.constant 1 : i16
    %37 = comb.shl %33, %36 : i16
    %38 = comb.extract %shift_amount from 0 : (i4) -> i1
    %39 = hw.constant 1 : i1
    %40 = comb.xor %38, %39 : i1
    %42 = hw.constant -1 : i1
    %41 = comb.xor %42, %40 : i1
    %44 = hw.array_create %33, %37 : i16
    %43 = hw.array_get %44[%41] : !hw.array<2xi16>
    hw.output %43 : i16
}
