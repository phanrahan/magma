hw.module @Register(%I: !hw.struct<x: i8, y: i1>, %CLK: i1) -> (%O: !hw.struct<x: i8, y: i1>) {
    %30 = sv.reg {name = "reg_P9_inst0"} : !hw.inout<i9>
    %31 = hw.constant 262 : i9
    %0 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %1 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %2 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %3 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %4 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %5 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %6 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %7 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %8 = hw.struct_extract %I["y"] : !hw.struct<x: i8, y: i1>
    %18 = sv.read_inout %30 : !hw.inout<i9>
    sv.initial { sv.bpassign %30, %31 : i9 }
    %9 = comb.extract %0 from 0 : (i8) -> i1
    %10 = comb.extract %1 from 1 : (i8) -> i1
    %11 = comb.extract %2 from 2 : (i8) -> i1
    %12 = comb.extract %3 from 3 : (i8) -> i1
    %13 = comb.extract %4 from 4 : (i8) -> i1
    %14 = comb.extract %5 from 5 : (i8) -> i1
    %15 = comb.extract %6 from 6 : (i8) -> i1
    %16 = comb.extract %7 from 7 : (i8) -> i1
    %19 = comb.extract %18 from 0 : (i9) -> i1
    %20 = comb.extract %18 from 1 : (i9) -> i1
    %21 = comb.extract %18 from 2 : (i9) -> i1
    %22 = comb.extract %18 from 3 : (i9) -> i1
    %23 = comb.extract %18 from 4 : (i9) -> i1
    %24 = comb.extract %18 from 5 : (i9) -> i1
    %25 = comb.extract %18 from 6 : (i9) -> i1
    %26 = comb.extract %18 from 7 : (i9) -> i1
    %27 = comb.extract %18 from 8 : (i9) -> i1
    %17 = comb.concat %8, %16, %15, %14, %13, %12, %11, %10, %9 : (i1, i1, i1, i1, i1, i1, i1, i1, i1) -> i9
    %28 = comb.concat %26, %25, %24, %23, %22, %21, %20, %19 : (i1, i1, i1, i1, i1, i1, i1, i1) -> i8
    sv.alwaysff(posedge %CLK) { sv.passign %30, %17 : i9 }
    %29 = hw.struct_create (%28, %27) : !hw.struct<x: i8, y: i1>
    hw.output %29 : !hw.struct<x: i8, y: i1>
}
