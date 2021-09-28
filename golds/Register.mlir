hw.module @Register(%I: !hw.struct<x: i8, y: i1>, %CLK: i1) -> (%O: !hw.struct<x: i8, y: i1>) {
    %0 = sv.reg {name = "reg_P9_inst0"} : !hw.inout<i9>
    %1 = hw.constant 262 : i9
    %2 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %3 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %4 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %5 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %6 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %7 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %8 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %9 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %10 = hw.struct_extract %I["y"] : !hw.struct<x: i8, y: i1>
    %11 = sv.read_inout %0 : !hw.inout<i9>
    sv.initial { sv.bpassign %0, %1 : i9 }
    %12 = comb.extract %2 from 0 : (i8) -> i1
    %13 = comb.extract %3 from 1 : (i8) -> i1
    %14 = comb.extract %4 from 2 : (i8) -> i1
    %15 = comb.extract %5 from 3 : (i8) -> i1
    %16 = comb.extract %6 from 4 : (i8) -> i1
    %17 = comb.extract %7 from 5 : (i8) -> i1
    %18 = comb.extract %8 from 6 : (i8) -> i1
    %19 = comb.extract %9 from 7 : (i8) -> i1
    %20 = comb.extract %11 from 0 : (i9) -> i1
    %21 = comb.extract %11 from 1 : (i9) -> i1
    %22 = comb.extract %11 from 2 : (i9) -> i1
    %23 = comb.extract %11 from 3 : (i9) -> i1
    %24 = comb.extract %11 from 4 : (i9) -> i1
    %25 = comb.extract %11 from 5 : (i9) -> i1
    %26 = comb.extract %11 from 6 : (i9) -> i1
    %27 = comb.extract %11 from 7 : (i9) -> i1
    %28 = comb.extract %11 from 8 : (i9) -> i1
    %29 = comb.concat %10, %19, %18, %17, %16, %15, %14, %13, %12 : (i1, i1, i1, i1, i1, i1, i1, i1, i1) -> i9
    %30 = comb.concat %27, %26, %25, %24, %23, %22, %21, %20 : (i1, i1, i1, i1, i1, i1, i1, i1) -> i8
    sv.alwaysff(posedge %CLK) { sv.passign %0, %29 : i9 }
    %31 = hw.struct_create (%30, %28) : !hw.struct<x: i8, y: i1>
    hw.output %31 : !hw.struct<x: i8, y: i1>
}
