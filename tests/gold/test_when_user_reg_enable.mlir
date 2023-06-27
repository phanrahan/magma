module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @Register(%I: i8, %CE: i1, %CLK: i1) -> (O: i8)
    hw.module @test_when_user_reg_enable(%I: i8, %x: i2, %CLK: i1) -> (O: i8) {
        %0 = comb.extract %x from 0 : (i2) -> i1
        %1 = hw.constant 1 : i1
        %2 = comb.extract %x from 1 : (i2) -> i1
        %4 = hw.constant -1 : i8
        %3 = comb.xor %4, %I : i8
        %5 = hw.constant 0 : i1
        %9 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i8>
        %7 = sv.read_inout %9 : !hw.inout<i8>
        %10 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %8 = sv.read_inout %10 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %9, %6 : i8
            sv.bpassign %10, %5 : i1
            sv.if %0 {
                sv.bpassign %9, %I : i8
                sv.bpassign %10, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %9, %3 : i8
                    sv.bpassign %10, %1 : i1
                }
            }
        }
        %6 = hw.instance "Register_inst0" @Register(I: %7: i8, CE: %8: i1, CLK: %CLK: i1) -> (O: i8)
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %7, %I) : i1, i8, i8
        %11 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %8, %11) : i1, i1, i1
        %13 = hw.constant -1 : i1
        %12 = comb.xor %13, %0 : i1
        %14 = comb.and %12, %2 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %7, %3) : i1, i8, i8
        %15 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %8, %15) : i1, i1, i1
        %16 = comb.or %0, %14 : i1
        %17 = comb.xor %13, %16 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%17, %7, %6) : i1, i8, i8
        %18 = comb.or %0, %14 : i1
        %19 = comb.xor %13, %18 : i1
        %20 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %8, %20) : i1, i1, i1
        hw.output %6 : i8
    }
}
