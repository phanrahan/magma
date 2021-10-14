hw.module @Register(%I: !hw.struct<x: i8, y: i1>, %CLK: i1) -> (%O: !hw.struct<x: i8, y: i1>) {
    %0 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %1 = comb.extract %0 from 0 : (i8) -> i1
    %2 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %3 = comb.extract %2 from 1 : (i8) -> i1
    %4 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %5 = comb.extract %4 from 2 : (i8) -> i1
    %6 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %7 = comb.extract %6 from 3 : (i8) -> i1
    %8 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %9 = comb.extract %8 from 4 : (i8) -> i1
    %10 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %11 = comb.extract %10 from 5 : (i8) -> i1
    %12 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %13 = comb.extract %12 from 6 : (i8) -> i1
    %14 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: i1>
    %15 = comb.extract %14 from 7 : (i8) -> i1
    %16 = hw.struct_extract %I["y"] : !hw.struct<x: i8, y: i1>
    %17 = comb.concat %16, %15, %13, %11, %9, %7, %5, %3, %1 : (i1, i1, i1, i1, i1, i1, i1, i1, i1) -> (i9)
    %19 = sv.reg {name = "reg_P9_inst0"} : !hw.inout<i9>
    sv.alwaysff(posedge %CLK) {
        sv.passign %19, %17 : i9
    }
    %18 = sv.read_inout %19 : !hw.inout<i9>
    %20 = comb.extract %18 from 0 : (i9) -> i1
    %21 = comb.extract %18 from 1 : (i9) -> i1
    %22 = comb.extract %18 from 2 : (i9) -> i1
    %23 = comb.extract %18 from 3 : (i9) -> i1
    %24 = comb.extract %18 from 4 : (i9) -> i1
    %25 = comb.extract %18 from 5 : (i9) -> i1
    %26 = comb.extract %18 from 6 : (i9) -> i1
    %27 = comb.extract %18 from 7 : (i9) -> i1
    %28 = comb.concat %27, %26, %25, %24, %23, %22, %21, %20 : (i1, i1, i1, i1, i1, i1, i1, i1) -> (i8)
    %29 = comb.extract %18 from 8 : (i9) -> i1
    %30 = hw.struct_create (%28, %29) : !hw.struct<x: i8, y: i1>
    hw.output %30 : !hw.struct<x: i8, y: i1>
}
