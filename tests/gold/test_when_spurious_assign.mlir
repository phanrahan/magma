module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_spurious_assign(%x: i8, %y: i1, %z: i2, %CLK: i1) -> (O_x: i8, O_y_x: i8, O_y_y: i1) {
        %0 = comb.extract %z from 0 : (i2) -> i1
        %1 = comb.extract %z from 1 : (i2) -> i1
        %2 = hw.constant 1 : i1
        %3 = hw.constant 1 : i8
        %5 = hw.constant -1 : i8
        %4 = comb.xor %5, %x : i8
        %8 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i8>
        %6 = sv.read_inout %8 : !hw.inout<i8>
        %9 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %7 = sv.read_inout %9 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %8, %x : i8
                } else {
                    sv.bpassign %8, %3 : i8
                }
            } else {
                sv.bpassign %8, %4 : i8
            }
        }
        %10 = hw.constant 1 : i1
        %12 = hw.constant -1 : i1
        %11 = comb.xor %12, %y : i1
        %15 = sv.reg name "_WHEN_WIRE_2" : !hw.inout<i1>
        %13 = sv.read_inout %15 : !hw.inout<i1>
        %16 = sv.reg name "_WHEN_WIRE_3" : !hw.inout<i1>
        %14 = sv.read_inout %16 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %1 {
                sv.bpassign %15, %y : i1
            } else {
                sv.bpassign %15, %11 : i1
            }
        }
        %20 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %20, %x : i8
            }
        }
        %21 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %20, %21 : i8
        }
        %17 = sv.read_inout %20 : !hw.inout<i8>
        %22 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %22, %6 : i8
            }
        }
        %23 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %22, %23 : i8
        }
        %18 = sv.read_inout %22 : !hw.inout<i8>
        %24 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %24, %13 : i1
            }
        }
        %25 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %24, %25 : i1
        }
        %19 = sv.read_inout %24 : !hw.inout<i1>
        %26 = comb.and %0, %1 : i1
        sv.verbatim "WHEN_ASSERT_199: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%26, %6, %x) : i1, i8, i8
        %27 = comb.xor %12, %1 : i1
        %28 = comb.and %0, %27 : i1
        %29 = hw.constant 1 : i8
        sv.verbatim "WHEN_ASSERT_200: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %6, %29) : i1, i8, i8
        %30 = comb.xor %12, %0 : i1
        sv.verbatim "WHEN_ASSERT_201: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %6, %4) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_202: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%1, %13, %y) : i1, i1, i1
        %31 = comb.xor %12, %1 : i1
        sv.verbatim "WHEN_ASSERT_203: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%31, %13, %11) : i1, i1, i1
        hw.output %17, %18, %19 : i8, i8, i1
    }
}
