module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_tuple_bulk_resolve(%I_x: i8, %I_y_x_x: i8, %I_y_x_y: i8, %I_y_y_x: i8, %I_y_y_y: i8, %S: i2, %CLK: i1) -> (O_x: i8, O_y_x_x: i8, O_y_x_y: i8, O_y_y_x: i8, O_y_y_y: i8) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %3 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i8>
        sv.assign %3, %1 : i8
        %2 = sv.read_inout %3 : !hw.inout<i8>
        %6 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i8>
        sv.assign %6, %4 : i8
        %5 = sv.read_inout %6 : !hw.inout<i8>
        %9 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i8>
        sv.assign %9, %7 : i8
        %8 = sv.read_inout %9 : !hw.inout<i8>
        %12 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_8 name "_WHEN_ASSERT_8" : !hw.inout<i8>
        sv.assign %12, %10 : i8
        %11 = sv.read_inout %12 : !hw.inout<i8>
        %15 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_9 name "_WHEN_ASSERT_9" : !hw.inout<i8>
        sv.assign %15, %13 : i8
        %14 = sv.read_inout %15 : !hw.inout<i8>
        %21 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %21, %2 : i8
        }
        %22 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %21, %22 : i8
        }
        %16 = sv.read_inout %21 : !hw.inout<i8>
        %23 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %23, %5 : i8
        }
        %24 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %23, %24 : i8
        }
        %17 = sv.read_inout %23 : !hw.inout<i8>
        %25 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %25, %8 : i8
        }
        %26 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %25, %26 : i8
        }
        %18 = sv.read_inout %25 : !hw.inout<i8>
        %27 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %27, %11 : i8
        }
        %28 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %27, %28 : i8
        }
        %19 = sv.read_inout %27 : !hw.inout<i8>
        %29 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %29, %14 : i8
        }
        %30 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %29, %30 : i8
        }
        %20 = sv.read_inout %29 : !hw.inout<i8>
        %31 = comb.extract %S from 1 : (i2) -> i1
        %42 = sv.reg : !hw.inout<i8>
        %37 = sv.read_inout %42 : !hw.inout<i8>
        %43 = sv.reg : !hw.inout<i8>
        %38 = sv.read_inout %43 : !hw.inout<i8>
        %44 = sv.reg : !hw.inout<i8>
        %39 = sv.read_inout %44 : !hw.inout<i8>
        %45 = sv.reg : !hw.inout<i8>
        %40 = sv.read_inout %45 : !hw.inout<i8>
        %46 = sv.reg : !hw.inout<i8>
        %41 = sv.read_inout %46 : !hw.inout<i8>
        %47 = sv.reg : !hw.inout<i8>
        %1 = sv.read_inout %47 : !hw.inout<i8>
        %48 = sv.reg : !hw.inout<i8>
        %4 = sv.read_inout %48 : !hw.inout<i8>
        %49 = sv.reg : !hw.inout<i8>
        %7 = sv.read_inout %49 : !hw.inout<i8>
        %50 = sv.reg : !hw.inout<i8>
        %10 = sv.read_inout %50 : !hw.inout<i8>
        %51 = sv.reg : !hw.inout<i8>
        %13 = sv.read_inout %51 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %42, %32 : i8
                sv.bpassign %47, %16 : i8
                sv.bpassign %43, %33 : i8
                sv.bpassign %44, %34 : i8
                sv.bpassign %45, %35 : i8
                sv.bpassign %46, %36 : i8
                sv.bpassign %48, %17 : i8
                sv.bpassign %49, %18 : i8
                sv.bpassign %50, %19 : i8
                sv.bpassign %51, %20 : i8
            } else {
                sv.bpassign %47, %32 : i8
                sv.bpassign %48, %33 : i8
                sv.bpassign %49, %34 : i8
                sv.bpassign %50, %35 : i8
                sv.bpassign %51, %36 : i8
                sv.if %31 {
                    sv.bpassign %42, %I_x : i8
                    sv.bpassign %43, %I_y_x_x : i8
                    sv.bpassign %44, %I_y_x_y : i8
                    sv.bpassign %45, %I_y_y_x : i8
                    sv.bpassign %46, %I_y_y_y : i8
                } else {
                    sv.bpassign %42, %32 : i8
                    sv.bpassign %43, %33 : i8
                    sv.bpassign %44, %34 : i8
                    sv.bpassign %45, %35 : i8
                    sv.bpassign %46, %36 : i8
                }
            }
        }
        %53 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %53, %37 : i8
        %52 = sv.read_inout %53 : !hw.inout<i8>
        %55 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i8>
        sv.assign %55, %38 : i8
        %54 = sv.read_inout %55 : !hw.inout<i8>
        %57 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i8>
        sv.assign %57, %39 : i8
        %56 = sv.read_inout %57 : !hw.inout<i8>
        %59 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i8>
        sv.assign %59, %40 : i8
        %58 = sv.read_inout %59 : !hw.inout<i8>
        %61 = sv.wire sym @test_when_tuple_bulk_resolve._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i8>
        sv.assign %61, %41 : i8
        %60 = sv.read_inout %61 : !hw.inout<i8>
        %62 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %62, %52 : i8
        }
        sv.initial {
            sv.bpassign %62, %22 : i8
        }
        %32 = sv.read_inout %62 : !hw.inout<i8>
        %63 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %63, %54 : i8
        }
        sv.initial {
            sv.bpassign %63, %24 : i8
        }
        %33 = sv.read_inout %63 : !hw.inout<i8>
        %64 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %64, %56 : i8
        }
        sv.initial {
            sv.bpassign %64, %26 : i8
        }
        %34 = sv.read_inout %64 : !hw.inout<i8>
        %65 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %65, %58 : i8
        }
        sv.initial {
            sv.bpassign %65, %28 : i8
        }
        %35 = sv.read_inout %65 : !hw.inout<i8>
        %66 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %66, %60 : i8
        }
        sv.initial {
            sv.bpassign %66, %30 : i8
        }
        %36 = sv.read_inout %66 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %52, %32) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %54, %33) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %56, %34) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %58, %35) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %60, %36) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %2, %16) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %5, %17) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %8, %18) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %11, %19) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %14, %20) : i1, i8, i8
        %68 = hw.constant -1 : i1
        %67 = comb.xor %68, %0 : i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%67, %2, %32) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%67, %5, %33) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%67, %8, %34) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%67, %11, %35) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%67, %14, %36) : i1, i8, i8
        %69 = comb.and %67, %31 : i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%69, %52, %I_x) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%69, %54, %I_y_x_x) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%69, %56, %I_y_x_y) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_18: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%69, %58, %I_y_y_x) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_19: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%69, %60, %I_y_y_y) : i1, i8, i8
        %70 = comb.xor %68, %31 : i1
        %71 = comb.and %67, %70 : i1
        sv.verbatim "WHEN_ASSERT_20: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%71, %52, %32) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_21: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%71, %54, %33) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_22: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%71, %56, %34) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_23: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%71, %58, %35) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_24: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%71, %60, %36) : i1, i8, i8
        hw.output %32, %33, %34, %35, %36 : i8, i8, i8, i8, i8
    }
}
