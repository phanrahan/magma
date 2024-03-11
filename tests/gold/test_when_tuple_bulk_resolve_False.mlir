module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_tuple_bulk_resolve_False(in %I: !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>, in %S: i2, in %CLK: i1, out O: !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %2 = hw.struct_extract %1["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %4 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i8>
        sv.assign %4, %2 : i8
        %3 = sv.read_inout %4 : !hw.inout<i8>
        %5 = hw.struct_extract %1["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %7 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<!hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.assign %7, %5 : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %6 = sv.read_inout %7 : !hw.inout<!hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %8 = hw.struct_create (%3, %6) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %10 = sv.reg name "y" : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %10, %8 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        %12 = hw.constant 0 : i8
        %15 = hw.constant 0 : i8
        %16 = hw.constant 0 : i8
        %14 = hw.struct_create (%15, %16) : !hw.struct<x: i8, y: i8>
        %18 = hw.constant 0 : i8
        %19 = hw.constant 0 : i8
        %17 = hw.struct_create (%18, %19) : !hw.struct<x: i8, y: i8>
        %13 = hw.struct_create (%14, %17) : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %11 = hw.struct_create (%12, %13) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.initial {
            sv.bpassign %10, %11 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        %9 = sv.read_inout %10 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %20 = comb.extract %S from 1 : (i2) -> i1
        %21 = hw.struct_extract %I["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %22 = hw.struct_extract %I["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %25 = sv.reg : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %24 = sv.read_inout %25 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %26 = sv.reg : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %1 = sv.read_inout %26 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        sv.alwayscomb {
            sv.if %0 {
                %31 = hw.struct_create (%27, %28) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.bpassign %25, %31 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                %32 = hw.struct_create (%29, %30) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.bpassign %26, %32 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
            } else {
                %33 = hw.struct_create (%27, %28) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.bpassign %26, %33 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                sv.if %20 {
                    %34 = hw.struct_create (%21, %22) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                    sv.bpassign %25, %34 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                } else {
                    %35 = hw.struct_create (%27, %28) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                    sv.bpassign %25, %35 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
                }
            }
        }
        %27 = hw.struct_extract %23["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %28 = hw.struct_extract %23["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %29 = hw.struct_extract %9["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %30 = hw.struct_extract %9["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %36 = hw.struct_extract %24["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %38 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %38, %36 : i8
        %37 = sv.read_inout %38 : !hw.inout<i8>
        %39 = hw.struct_extract %24["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %41 = sv.wire sym @test_when_tuple_bulk_resolve_False._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<!hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.assign %41, %39 : !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %40 = sv.read_inout %41 : !hw.inout<!hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %42 = hw.struct_create (%37, %40) : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        %43 = sv.reg name "x" : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %43, %42 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        sv.initial {
            sv.bpassign %43, %11 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        }
        %23 = sv.read_inout %43 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>>
        %44 = hw.struct_extract %23["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %37, %44) : i1, i8, i8
        %45 = hw.struct_extract %23["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %40, %45) : i1, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %46 = hw.struct_extract %9["x"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %3, %46) : i1, i8, i8
        %47 = hw.struct_extract %9["y"] : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %6, %47) : i1, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %49 = hw.constant -1 : i1
        %48 = comb.xor %49, %0 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%48, %3, %44) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%48, %6, %45) : i1, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %50 = comb.and %48, %20 : i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%50, %37, %21) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%50, %40, %22) : i1, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        %51 = comb.xor %49, %20 : i1
        %52 = comb.and %48, %51 : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%52, %37, %44) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%52, %40, %45) : i1, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>, !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>
        hw.output %23 : !hw.struct<x: i8, y: !hw.struct<x: !hw.struct<x: i8, y: i8>, y: !hw.struct<x: i8, y: i8>>>
    }
}
