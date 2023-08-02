module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_spurious_assign(%x: i8, %y: i1, %z: i2, %CLK: i1) -> (O_x: i8, O_y_x: i8, O_y_y: i1) {
        %0 = comb.extract %z from 0 : (i2) -> i1
        %1 = comb.extract %z from 1 : (i2) -> i1
        %2 = hw.constant 1 : i1
        %3 = hw.constant 1 : i8
        %5 = hw.constant -1 : i8
        %4 = comb.xor %5, %x : i8
        %8 = sv.reg : !hw.inout<i8>
        %6 = sv.read_inout %8 : !hw.inout<i8>
        %9 = sv.reg : !hw.inout<i1>
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
        %11 = sv.wire sym @test_when_spurious_assign._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %11, %6 : i8
        %10 = sv.read_inout %11 : !hw.inout<i8>
        %12 = hw.constant 1 : i1
        %14 = hw.constant -1 : i1
        %13 = comb.xor %14, %y : i1
        %17 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %18 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %1 {
                sv.bpassign %17, %y : i1
            } else {
                sv.bpassign %17, %13 : i1
            }
        }
        %20 = sv.wire sym @test_when_spurious_assign._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %20, %15 : i1
        %19 = sv.read_inout %20 : !hw.inout<i1>
        %24 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %24, %x : i8
            }
        }
        %25 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %24, %25 : i8
        }
        %21 = sv.read_inout %24 : !hw.inout<i8>
        %26 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %26, %10 : i8
            }
        }
        %27 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %26, %27 : i8
        }
        %22 = sv.read_inout %26 : !hw.inout<i8>
        %28 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %28, %19 : i1
            }
        }
        %29 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %28, %29 : i1
        }
        %23 = sv.read_inout %28 : !hw.inout<i1>
        %30 = comb.and %0, %1 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %10, %x) : i1, i8, i8
        %31 = comb.xor %14, %1 : i1
        %32 = comb.and %0, %31 : i1
        %33 = hw.constant 1 : i8
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %10, %33) : i1, i8, i8
        %34 = comb.xor %14, %0 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%34, %10, %4) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%1, %19, %y) : i1, i1, i1
        %35 = comb.xor %14, %1 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%35, %19, %13) : i1, i1, i1
        hw.output %21, %22, %23 : i8, i8, i1
    }
}
