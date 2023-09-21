module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_reg_ce_implicit_wire_twice(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %0 = hw.constant 1 : i1
        %1 = hw.constant 0 : i1
        %5 = sv.reg : !hw.inout<i8>
        %3 = sv.read_inout %5 : !hw.inout<i8>
        %6 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %6 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i8
            sv.if %y {
                sv.bpassign %5, %I : i8
            }
        }
        %8 = sv.wire sym @test_when_reg_ce_implicit_wire_twice._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %8, %3 : i8
        %7 = sv.read_inout %8 : !hw.inout<i8>
        %10 = hw.constant -1 : i8
        %9 = comb.xor %10, %I : i8
        %12 = sv.wire sym @test_when_reg_ce_implicit_wire_twice._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %12, %4 : i1
        %11 = sv.read_inout %12 : !hw.inout<i1>
        %13 = hw.constant 1 : i1
        %16 = sv.reg : !hw.inout<i8>
        %14 = sv.read_inout %16 : !hw.inout<i8>
        %17 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %17 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %16, %7 : i8
            sv.if %x {
                sv.bpassign %16, %9 : i8
            }
        }
        %19 = sv.wire sym @test_when_reg_ce_implicit_wire_twice._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %19, %14 : i8
        %18 = sv.read_inout %19 : !hw.inout<i8>
        %21 = sv.wire sym @test_when_reg_ce_implicit_wire_twice._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %21, %15 : i1
        %20 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %20 {
                sv.passign %22, %18 : i8
            }
        }
        %23 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %22, %23 : i8
        }
        %2 = sv.read_inout %22 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %7, %I) : i1, i8, i8
        %24 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %11, %24) : i1, i1, i1
        %26 = hw.constant -1 : i1
        %25 = comb.xor %26, %y : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%25, %7, %2) : i1, i8, i8
        %27 = comb.xor %26, %y : i1
        %28 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %11, %28) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %18, %9) : i1, i8, i8
        %29 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %20, %29) : i1, i1, i1
        %30 = comb.xor %26, %x : i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %18, %3) : i1, i8, i8
        hw.output %2 : i8
    }
}
