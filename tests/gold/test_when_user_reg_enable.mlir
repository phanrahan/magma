module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module.extern @Register(in %I: i8, in %CE: i1, in %CLK: i1, out O: i8)
    hw.module @test_when_user_reg_enable(in %I: i8, in %x: i2, in %CLK: i1, out O: i8) {
        %0 = comb.extract %x from 0 : (i2) -> i1
        %1 = hw.constant 1 : i1
        %2 = comb.extract %x from 1 : (i2) -> i1
        %4 = hw.constant -1 : i8
        %3 = comb.xor %4, %I : i8
        %5 = hw.constant 0 : i1
        %9 = sv.reg : !hw.inout<i8>
        %7 = sv.read_inout %9 : !hw.inout<i8>
        %10 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %10 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %9, %6 : i8
            sv.if %0 {
                sv.bpassign %9, %I : i8
            } else {
                sv.if %2 {
                    sv.bpassign %9, %3 : i8
                }
            }
        }
        %12 = sv.wire sym @test_when_user_reg_enable._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %12, %7 : i8
        %11 = sv.read_inout %12 : !hw.inout<i8>
        %14 = sv.wire sym @test_when_user_reg_enable._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %14, %8 : i1
        %13 = sv.read_inout %14 : !hw.inout<i1>
        %6 = hw.instance "Register_inst0" @Register(I: %11: i8, CE: %13: i1, CLK: %CLK: i1) -> (O: i8)
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %11, %I) : i1, i8, i8
        %15 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %13, %15) : i1, i1, i1
        %17 = hw.constant -1 : i1
        %16 = comb.xor %17, %0 : i1
        %18 = comb.and %16, %2 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%18, %11, %3) : i1, i8, i8
        %19 = comb.or %0, %18 : i1
        %20 = comb.xor %17, %19 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%20, %11, %6) : i1, i8, i8
        hw.output %6 : i8
    }
}
