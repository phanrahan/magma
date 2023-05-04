module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_array_assign_False(%I: !hw.struct<x: i1, y: !hw.struct<_0: i1, _1: i8>>, %S: i1) -> (O: !hw.struct<x: i1, y: !hw.struct<_0: i1, _1: i8>>) {
        %0 = hw.struct_extract %I["x"] : !hw.struct<x: i1, y: !hw.struct<_0: i1, _1: i8>>
        %1 = hw.struct_extract %I["y"] : !hw.struct<x: i1, y: !hw.struct<_0: i1, _1: i8>>
        %2 = hw.struct_extract %1["_0"] : !hw.struct<_0: i1, _1: i8>
        %3 = hw.struct_extract %1["_1"] : !hw.struct<_0: i1, _1: i8>
        %5 = sv.reg : !hw.inout<i8>
        %4 = sv.read_inout %5 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %S {
                %14 = comb.concat %13, %12, %11, %10, %9, %8, %7, %6 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %5, %14 : i8
            } else {
                %15 = comb.concat %6, %7, %8, %9, %10, %11, %12, %13 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %5, %15 : i8
            }
        }
        %6 = comb.extract %3 from 0 : (i8) -> i1
        %7 = comb.extract %3 from 1 : (i8) -> i1
        %8 = comb.extract %3 from 2 : (i8) -> i1
        %9 = comb.extract %3 from 3 : (i8) -> i1
        %10 = comb.extract %3 from 4 : (i8) -> i1
        %11 = comb.extract %3 from 5 : (i8) -> i1
        %12 = comb.extract %3 from 6 : (i8) -> i1
        %13 = comb.extract %3 from 7 : (i8) -> i1
        %16 = hw.struct_create (%2, %4) : !hw.struct<_0: i1, _1: i8>
        %17 = hw.struct_create (%0, %16) : !hw.struct<x: i1, y: !hw.struct<_0: i1, _1: i8>>
        hw.output %17 : !hw.struct<x: i1, y: !hw.struct<_0: i1, _1: i8>>
    }
}
