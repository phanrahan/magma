module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_emit_asserts_value(%S: i3, %O_ready: i1, %CLK: i1) -> (O_valid: i1, O_data_x: i1, O_data_y: i8) {
        %0 = hw.constant 0 : i1
        %1 = comb.extract %S from 0 : (i3) -> i1
        %2 = comb.extract %S from 1 : (i3) -> i1
        %5 = sv.wire sym @test_when_emit_asserts_value._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i8>
        sv.assign %5, %3 : i8
        %4 = sv.read_inout %5 : !hw.inout<i8>
        %6 = comb.extract %S from 2 : (i3) -> i1
        %12 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %12 : !hw.inout<i1>
        %13 = sv.reg : !hw.inout<i8>
        %11 = sv.read_inout %13 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %12, %8 : i1
            sv.bpassign %13, %9 : i8
            sv.if %1 {
                sv.if %2 {
                    sv.bpassign %12, %7 : i1
                    sv.bpassign %13, %4 : i8
                } else {
                    sv.if %6 {
                        sv.bpassign %12, %7 : i1
                        sv.bpassign %13, %4 : i8
                    }
                }
            }
        }
        %15 = sv.wire sym @test_when_emit_asserts_value._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %15, %10 : i1
        %14 = sv.read_inout %15 : !hw.inout<i1>
        %17 = sv.wire sym @test_when_emit_asserts_value._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i8>
        sv.assign %17, %11 : i8
        %16 = sv.read_inout %17 : !hw.inout<i8>
        %18 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %18, %14 : i1
        }
        %19 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %18, %19 : i1
        }
        %8 = sv.read_inout %18 : !hw.inout<i1>
        %20 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %20, %16 : i8
        }
        %21 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %20, %21 : i8
        }
        %9 = sv.read_inout %20 : !hw.inout<i8>
        %22 = hw.constant 0 : i1
        %23 = hw.constant 1 : i1
        %25 = hw.array_create %23, %22 : i1
        %24 = hw.array_get %25[%2] : !hw.array<2xi1>, i1
        %26 = hw.constant 0 : i8
        %27 = hw.constant 1 : i8
        %29 = hw.array_create %27, %26 : i8
        %28 = hw.array_get %29[%6] : !hw.array<2xi8>, i1
        %31 = sv.reg : !hw.inout<i1>
        %30 = sv.read_inout %31 : !hw.inout<i1>
        %32 = sv.reg : !hw.inout<i8>
        %3 = sv.read_inout %32 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %1 {
                sv.bpassign %31, %8 : i1
                sv.bpassign %32, %9 : i8
            } else {
                sv.bpassign %31, %24 : i1
                sv.bpassign %32, %28 : i8
            }
        }
        %33 = sv.wire sym @test_when_emit_asserts_value._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %33, %30 : i1
        %7 = sv.read_inout %33 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%1, %7, %8) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%1, %4, %9) : i1, i8, i8
        %35 = hw.constant -1 : i1
        %34 = comb.xor %35, %1 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%34, %7, %24) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%34, %4, %28) : i1, i8, i8
        %36 = comb.and %1, %2 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%36, %14, %30) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%36, %16, %3) : i1, i8, i8
        %37 = comb.xor %35, %2 : i1
        %38 = comb.and %1, %37 : i1
        %39 = comb.and %38, %6 : i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%39, %14, %30) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%39, %16, %3) : i1, i8, i8
        %40 = comb.or %36, %39 : i1
        %41 = comb.xor %35, %40 : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %14, %8) : i1, i1, i1
        %42 = comb.or %36, %39 : i1
        %43 = comb.xor %35, %42 : i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%43, %16, %9) : i1, i8, i8
        hw.output %0, %7, %4 : i1, i1, i8
    }
}
