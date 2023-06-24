module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_value(%S: i3, %O_ready: i1, %CLK: i1) -> (O_valid: i1, O_data_x: i1, O_data_y: i8) {
        %0 = hw.constant 0 : i1
        %1 = comb.extract %S from 0 : (i3) -> i1
        %2 = comb.extract %S from 1 : (i3) -> i1
        %3 = comb.extract %S from 2 : (i3) -> i1
        %10 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i1>
        %8 = sv.read_inout %10 : !hw.inout<i1>
        %11 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i8>
        %9 = sv.read_inout %11 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %10, %6 : i1
            sv.bpassign %11, %7 : i8
            sv.if %1 {
                sv.if %2 {
                    sv.bpassign %10, %4 : i1
                    sv.bpassign %11, %5 : i8
                } else {
                    sv.if %3 {
                        sv.bpassign %10, %4 : i1
                        sv.bpassign %11, %5 : i8
                    }
                }
            }
        }
        %12 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %12, %8 : i1
        }
        %13 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %12, %13 : i1
        }
        %6 = sv.read_inout %12 : !hw.inout<i1>
        %14 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %14, %9 : i8
        }
        %15 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %14, %15 : i8
        }
        %7 = sv.read_inout %14 : !hw.inout<i8>
        %16 = hw.constant 0 : i1
        %17 = hw.constant 1 : i1
        %19 = hw.array_create %17, %16 : i1
        %18 = hw.array_get %19[%2] : !hw.array<2xi1>, i1
        %20 = hw.constant 0 : i8
        %21 = hw.constant 1 : i8
        %23 = hw.array_create %21, %20 : i8
        %22 = hw.array_get %23[%3] : !hw.array<2xi8>, i1
        %24 = sv.reg name "_WHEN_WIRE_2" : !hw.inout<i1>
        %4 = sv.read_inout %24 : !hw.inout<i1>
        %25 = sv.reg name "_WHEN_WIRE_3" : !hw.inout<i8>
        %5 = sv.read_inout %25 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %1 {
                sv.bpassign %24, %6 : i1
                sv.bpassign %25, %7 : i8
            } else {
                sv.bpassign %24, %18 : i1
                sv.bpassign %25, %22 : i8
            }
        }
        sv.verbatim "WHEN_ASSERT_442: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%1, %4, %6) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_443: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%1, %5, %7) : i1, i8, i8
        %27 = hw.constant -1 : i1
        %26 = comb.xor %27, %1 : i1
        sv.verbatim "WHEN_ASSERT_444: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%26, %4, %18) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_445: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%26, %5, %22) : i1, i8, i8
        %28 = comb.and %1, %2 : i1
        sv.verbatim "WHEN_ASSERT_446: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %8, %4) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_447: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %9, %5) : i1, i8, i8
        %29 = comb.xor %27, %2 : i1
        %30 = comb.and %1, %29 : i1
        %31 = comb.and %30, %3 : i1
        sv.verbatim "WHEN_ASSERT_448: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%31, %8, %4) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_449: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%31, %9, %5) : i1, i8, i8
        %32 = comb.or %28, %31 : i1
        %33 = comb.xor %27, %32 : i1
        sv.verbatim "WHEN_ASSERT_450: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%33, %8, %6) : i1, i1, i1
        %34 = comb.or %28, %31 : i1
        %35 = comb.xor %27, %34 : i1
        sv.verbatim "WHEN_ASSERT_451: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%35, %9, %7) : i1, i8, i8
        hw.output %0, %4, %5 : i1, i1, i8
    }
}
