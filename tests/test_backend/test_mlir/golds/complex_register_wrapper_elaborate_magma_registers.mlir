hw.module @Register(%I: !hw.struct<x: i8, y: i1>, %CE: i1, %CLK: i1, %ASYNCRESET: i1) -> (O: !hw.struct<x: i8, y: i1>) {
    %1 = comb.extract %0 from 1 : (i9) -> i1
    %2 = comb.extract %0 from 2 : (i9) -> i1
    %3 = comb.extract %0 from 3 : (i9) -> i1
    %4 = comb.extract %0 from 4 : (i9) -> i1
    %5 = comb.extract %0 from 5 : (i9) -> i1
    %6 = comb.extract %0 from 6 : (i9) -> i1
    %7 = comb.extract %0 from 7 : (i9) -> i1
    %9 = comb.concat %7, %6, %5, %4, %3, %2, %1, %8 : i1, i1, i1, i1, i1, i1, i1, i1
    %10 = comb.extract %0 from 8 : (i9) -> i1
    %11 = hw.struct_create (%9, %10) : !hw.struct<x: i8, y: i1>
    %13 = hw.array_create %11, %I : !hw.struct<x: i8, y: i1>
    %12 = hw.array_get %13[%CE] : !hw.array<2x!hw.struct<x: i8, y: i1>>
    %14 = hw.struct_extract %12["x"] : !hw.struct<x: i8, y: i1>
    %15 = comb.extract %14 from 0 : (i8) -> i1
    %16 = comb.extract %14 from 1 : (i8) -> i1
    %17 = comb.extract %14 from 2 : (i8) -> i1
    %18 = comb.extract %14 from 3 : (i8) -> i1
    %19 = comb.extract %14 from 4 : (i8) -> i1
    %20 = comb.extract %14 from 5 : (i8) -> i1
    %21 = comb.extract %14 from 6 : (i8) -> i1
    %22 = comb.extract %14 from 7 : (i8) -> i1
    %23 = hw.struct_extract %12["y"] : !hw.struct<x: i8, y: i1>
    %24 = comb.concat %23, %22, %21, %20, %19, %18, %17, %16, %15 : i1, i1, i1, i1, i1, i1, i1, i1, i1
    %25 = sv.reg {name = "reg_PR9_inst0"} : !hw.inout<i9>
    sv.alwaysff(posedge %CLK) {
        sv.passign %25, %24 : i9
    } (asyncreset : posedge %ASYNCRESET) {
        sv.passign %25, %26 : i9
    }
    %26 = hw.constant 266 : i9
    sv.initial {
        sv.bpassign %25, %26 : i9
    }
    %0 = sv.read_inout %25 : !hw.inout<i9>
    %8 = comb.extract %0 from 0 : (i9) -> i1
    %27 = comb.concat %7, %6, %5, %4, %3, %2, %1, %8 : i1, i1, i1, i1, i1, i1, i1, i1
    %28 = hw.struct_create (%27, %10) : !hw.struct<x: i8, y: i1>
    hw.output %28 : !hw.struct<x: i8, y: i1>
}
hw.module @complex_register_wrapper(%a: !hw.struct<x: i8, y: i1>, %b: !hw.array<6xi16>, %CLK: i1, %CE: i1, %ASYNCRESET: i1) -> (y: !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>) {
    %0 = hw.instance "Register_inst0" @Register(I: %a: !hw.struct<x: i8, y: i1>, CE: %CE: i1, CLK: %CLK: i1, ASYNCRESET: %ASYNCRESET: i1) -> (O: !hw.struct<x: i8, y: i1>)
    %1 = hw.instance "Register_inst1" @Register(I: %b: !hw.array<6xi16>, CE: %CLK: i1) -> (O: !hw.array<6xi16>)
    %2 = hw.struct_create (%0, %1) : !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>
    %3 = hw.struct_extract %a["x"] : !hw.struct<x: i8, y: i1>
    %4 = hw.instance "Register_inst2" @Register(I: %3: i8, CE: %CE: i1, CLK: %CLK: i1) -> (O: i8)
    hw.output %2 : !hw.struct<u: !hw.struct<x: i8, y: i1>, v: !hw.array<6xi16>>
}
