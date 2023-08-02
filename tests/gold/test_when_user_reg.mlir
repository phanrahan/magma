module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @Register(%I: i8, %CLK: i1) -> (O: i8)
    hw.module @test_when_user_reg(%I: i8, %x: i1, %CLK: i1) -> (O: i8) {
        %2 = sv.reg : !hw.inout<i8>
        %1 = sv.read_inout %2 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %2, %0 : i8
            sv.if %x {
                sv.bpassign %2, %I : i8
            }
        }
        %4 = sv.wire sym @test_when_user_reg._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %4, %1 : i8
        %3 = sv.read_inout %4 : !hw.inout<i8>
        %0 = hw.instance "Register_inst0" @Register(I: %3: i8, CLK: %CLK: i1) -> (O: i8)
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %3, %I) : i1, i8, i8
        %6 = hw.constant -1 : i1
        %5 = comb.xor %6, %x : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%5, %3, %0) : i1, i8, i8
        hw.output %0 : i8
    }
}
