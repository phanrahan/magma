module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_reg_ce_implicit_wire_twice(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %0 = hw.constant 1 : i1
        %1 = hw.constant 0 : i1
        %5 = sv.reg name "_WHEN_WIRE_92" : !hw.inout<i8>
        %3 = sv.read_inout %5 : !hw.inout<i8>
        %6 = sv.reg name "_WHEN_WIRE_93" : !hw.inout<i1>
        %4 = sv.read_inout %6 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i8
            sv.bpassign %6, %1 : i1
            sv.if %y {
                sv.bpassign %5, %I : i8
                sv.bpassign %6, %0 : i1
            }
        }
        %8 = hw.constant -1 : i8
        %7 = comb.xor %8, %I : i8
        %9 = hw.constant 1 : i1
        %12 = sv.reg name "_WHEN_WIRE_94" : !hw.inout<i8>
        %10 = sv.read_inout %12 : !hw.inout<i8>
        %13 = sv.reg name "_WHEN_WIRE_95" : !hw.inout<i1>
        %11 = sv.read_inout %13 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %12, %3 : i8
            sv.bpassign %13, %4 : i1
            sv.if %x {
                sv.bpassign %12, %7 : i8
                sv.bpassign %13, %9 : i1
            }
        }
        %14 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %11 {
                sv.passign %14, %10 : i8
            }
        }
        %15 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %14, %15 : i8
        }
        %2 = sv.read_inout %14 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_134: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %3, %I) : i1, i8, i8
        %16 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_135: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %4, %16) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_136: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %10, %7) : i1, i8, i8
        %17 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_137: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %11, %17) : i1, i1, i1
        hw.output %2 : i8
    }
}
