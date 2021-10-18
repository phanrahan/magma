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
    %9 = hw.instance "Register_inst0" @Register(%7, %CLK) : (i16, i1) -> (i16)
    %10 = hw.constant 4 : i16
    %11 = comb.shl %9, %10 : i16
    %12 = comb.extract %shift_amount from 2 : (i4) -> i1
    %13 = hw.constant 1 : i1
    %14 = comb.xor %12, %13 : i1
    %16 = hw.constant -1 : i1
    %15 = comb.xor %16, %14 : i1
    %18 = hw.array_create %9, %11 : i16
    %17 = hw.array_get %18[%15] : !hw.array<2xi16>
    %19 = hw.instance "Register_inst1" @Register(%17, %CLK) : (i16, i1) -> (i16)
    %20 = hw.constant 2 : i16
    %21 = comb.shl %19, %20 : i16
    %22 = comb.extract %shift_amount from 1 : (i4) -> i1
    %23 = hw.constant 1 : i1
    %24 = comb.xor %22, %23 : i1
    %26 = hw.constant -1 : i1
    %25 = comb.xor %26, %24 : i1
    %28 = hw.array_create %19, %21 : i16
    %27 = hw.array_get %28[%25] : !hw.array<2xi16>
    %29 = hw.instance "Register_inst2" @Register(%27, %CLK) : (i16, i1) -> (i16)
    %30 = hw.constant 1 : i16
    %31 = comb.shl %29, %30 : i16
    %32 = comb.extract %shift_amount from 0 : (i4) -> i1
    %33 = hw.constant 1 : i1
    %34 = comb.xor %32, %33 : i1
    %36 = hw.constant -1 : i1
    %35 = comb.xor %36, %34 : i1
    %38 = hw.array_create %29, %31 : i16
    %37 = hw.array_get %38[%35] : !hw.array<2xi16>
    hw.output %37 : i16
}
