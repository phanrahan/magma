module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_partial_assign_order(%I: i2, %S: i2) -> (O0: i2, O1: i2, O2: i2) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %2 = hw.constant -1 : i2
        %1 = comb.xor %2, %I : i2
        %3 = comb.extract %1 from 1 : (i2) -> i1
        %4 = comb.extract %1 from 0 : (i2) -> i1
        %5 = comb.extract %S from 1 : (i2) -> i1
        %6 = comb.xor %2, %I : i2
        %7 = comb.extract %6 from 0 : (i2) -> i1
        %8 = comb.extract %6 from 1 : (i2) -> i1
        %9 = comb.xor %2, %I : i2
        %10 = comb.extract %9 from 0 : (i2) -> i1
        %11 = comb.extract %9 from 1 : (i2) -> i1
        %17 = sv.reg name "_WHEN_WIRE_122" : !hw.inout<i1>
        %12 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg name "_WHEN_WIRE_123" : !hw.inout<i1>
        %13 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg name "_WHEN_WIRE_124" : !hw.inout<i2>
        %14 = sv.read_inout %19 : !hw.inout<i2>
        %20 = sv.reg name "_WHEN_WIRE_125" : !hw.inout<i1>
        %15 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg name "_WHEN_WIRE_126" : !hw.inout<i1>
        %16 = sv.read_inout %21 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %20, %22 : i1
            sv.bpassign %21, %23 : i1
            sv.if %0 {
                sv.bpassign %17, %3 : i1
                sv.bpassign %18, %4 : i1
                %24 = comb.concat %23, %22 : i1, i1
                sv.bpassign %19, %24 : i2
            } else {
                sv.if %5 {
                    sv.bpassign %17, %22 : i1
                    sv.bpassign %18, %23 : i1
                    %25 = comb.concat %23, %22 : i1, i1
                    sv.bpassign %19, %25 : i2
                } else {
                    sv.bpassign %17, %7 : i1
                    sv.bpassign %18, %8 : i1
                    sv.bpassign %20, %23 : i1
                    sv.bpassign %21, %22 : i1
                    %26 = comb.concat %11, %10 : i1, i1
                    sv.bpassign %19, %26 : i2
                }
            }
        }
        %22 = comb.extract %I from 0 : (i2) -> i1
        %23 = comb.extract %I from 1 : (i2) -> i1
        %27 = comb.concat %16, %15 : i1, i1
        %28 = comb.concat %13, %12 : i1, i1
        sv.verbatim "WHEN_ASSERT_247: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %12, %3) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_248: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %13, %4) : i1, i1, i1
        %29 = comb.extract %14 from 0 : (i2) -> i1
        %30 = comb.extract %I from 0 : (i2) -> i1
        sv.verbatim "WHEN_ASSERT_249: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %29, %30) : i1, i1, i1
        %31 = comb.extract %14 from 1 : (i2) -> i1
        %32 = comb.extract %I from 1 : (i2) -> i1
        sv.verbatim "WHEN_ASSERT_250: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %31, %32) : i1, i1, i1
        %34 = hw.constant -1 : i1
        %33 = comb.xor %34, %0 : i1
        %35 = comb.and %33, %5 : i1
        sv.verbatim "WHEN_ASSERT_251: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%35, %12, %30) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_252: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%35, %13, %32) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_253: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%35, %29, %30) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_254: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%35, %31, %32) : i1, i1, i1
        %36 = comb.xor %34, %5 : i1
        %37 = comb.and %33, %36 : i1
        sv.verbatim "WHEN_ASSERT_255: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%37, %12, %7) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_256: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%37, %13, %8) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_257: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%37, %15, %32) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_258: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%37, %16, %30) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_259: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%37, %29, %10) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_260: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%37, %31, %11) : i1, i1, i1
        %38 = comb.xor %34, %37 : i1
        sv.verbatim "WHEN_ASSERT_261: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%38, %15, %30) : i1, i1, i1
        %39 = comb.xor %34, %37 : i1
        sv.verbatim "WHEN_ASSERT_262: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%39, %16, %32) : i1, i1, i1
        hw.output %27, %28, %14 : i2, i2, i2
    }
}
