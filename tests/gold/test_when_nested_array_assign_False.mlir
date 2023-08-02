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
        %16 = comb.extract %4 from 0 : (i8) -> i1
        %18 = sv.wire sym @test_when_nested_array_assign_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %18, %16 : i1
        %17 = sv.read_inout %18 : !hw.inout<i1>
        %19 = comb.extract %4 from 1 : (i8) -> i1
        %21 = sv.wire sym @test_when_nested_array_assign_False._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %21, %19 : i1
        %20 = sv.read_inout %21 : !hw.inout<i1>
        %22 = comb.extract %4 from 2 : (i8) -> i1
        %24 = sv.wire sym @test_when_nested_array_assign_False._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %24, %22 : i1
        %23 = sv.read_inout %24 : !hw.inout<i1>
        %25 = comb.extract %4 from 3 : (i8) -> i1
        %27 = sv.wire sym @test_when_nested_array_assign_False._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %27, %25 : i1
        %26 = sv.read_inout %27 : !hw.inout<i1>
        %28 = comb.extract %4 from 4 : (i8) -> i1
        %30 = sv.wire sym @test_when_nested_array_assign_False._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %30, %28 : i1
        %29 = sv.read_inout %30 : !hw.inout<i1>
        %31 = comb.extract %4 from 5 : (i8) -> i1
        %33 = sv.wire sym @test_when_nested_array_assign_False._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i1>
        sv.assign %33, %31 : i1
        %32 = sv.read_inout %33 : !hw.inout<i1>
        %34 = comb.extract %4 from 6 : (i8) -> i1
        %36 = sv.wire sym @test_when_nested_array_assign_False._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i1>
        sv.assign %36, %34 : i1
        %35 = sv.read_inout %36 : !hw.inout<i1>
        %37 = comb.extract %4 from 7 : (i8) -> i1
        %39 = sv.wire sym @test_when_nested_array_assign_False._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i1>
        sv.assign %39, %37 : i1
        %38 = sv.read_inout %39 : !hw.inout<i1>
        %40 = comb.concat %38, %35, %32, %29, %26, %23, %20, %17 : i1, i1, i1, i1, i1, i1, i1, i1
        %41 = hw.struct_create (%2, %40) : !hw.struct<_0: i1, _1: i8>
        %42 = hw.struct_create (%0, %41) : !hw.struct<x: i1, y: !hw.struct<_0: i1, _1: i8>>
        %43 = comb.extract %3 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %17, %43) : i1, i1, i1
        %44 = comb.extract %3 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %20, %44) : i1, i1, i1
        %45 = comb.extract %3 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %23, %45) : i1, i1, i1
        %46 = comb.extract %3 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %26, %46) : i1, i1, i1
        %47 = comb.extract %3 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %29, %47) : i1, i1, i1
        %48 = comb.extract %3 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %32, %48) : i1, i1, i1
        %49 = comb.extract %3 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %35, %49) : i1, i1, i1
        %50 = comb.extract %3 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %38, %50) : i1, i1, i1
        %52 = hw.constant -1 : i1
        %51 = comb.xor %52, %S : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %17, %50) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %20, %49) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %23, %48) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %26, %47) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %29, %46) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %32, %45) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %35, %44) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %38, %43) : i1, i1, i1
        hw.output %42 : !hw.struct<x: i1, y: !hw.struct<_0: i1, _1: i8>>
    }
}
