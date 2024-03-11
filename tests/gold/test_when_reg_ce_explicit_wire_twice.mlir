module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_reg_ce_explicit_wire_twice(in %I: i8, in %x: i1, in %y: i1, in %CLK: i1, out O: i8) {
        %2 = sv.reg : !hw.inout<i8>
        %1 = sv.read_inout %2 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %2, %0 : i8
            sv.if %y {
                sv.bpassign %2, %I : i8
            }
        }
        %4 = sv.wire sym @test_when_reg_ce_explicit_wire_twice._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %4, %1 : i8
        %3 = sv.read_inout %4 : !hw.inout<i8>
        %6 = hw.constant -1 : i8
        %5 = comb.xor %6, %I : i8
        %8 = sv.reg : !hw.inout<i8>
        %7 = sv.read_inout %8 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %8, %3 : i8
            sv.if %x {
                sv.bpassign %8, %5 : i8
            }
        }
        %10 = sv.wire sym @test_when_reg_ce_explicit_wire_twice._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %10, %7 : i8
        %9 = sv.read_inout %10 : !hw.inout<i8>
        %12 = hw.constant -1 : i1
        %11 = comb.xor %12, %y : i1
        %13 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %11 {
                sv.passign %13, %9 : i8
            }
        }
        %14 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %13, %14 : i8
        }
        %0 = sv.read_inout %13 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %3, %I) : i1, i8, i8
        %15 = comb.xor %12, %y : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%15, %3, %0) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %9, %5) : i1, i8, i8
        %16 = comb.xor %12, %x : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%16, %9, %1) : i1, i8, i8
        hw.output %0 : i8
    }
}
