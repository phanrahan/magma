module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Gen(%a: i8) -> (y: i8) {
        %0 = comb.extract %a from 0 : (i8) -> i1
        %1 = comb.extract %a from 1 : (i8) -> i1
        %2 = hw.constant 0 : i1
        %3 = comb.extract %a from 2 : (i8) -> i1
        %4 = comb.extract %a from 3 : (i8) -> i1
        %5 = comb.extract %a from 4 : (i8) -> i1
        %6 = comb.extract %a from 5 : (i8) -> i1
        %7 = comb.extract %a from 6 : (i8) -> i1
        %8 = comb.extract %a from 7 : (i8) -> i1
        %17 = sv.reg name "_WHEN_WIRE_132" : !hw.inout<i1>
        %9 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg name "_WHEN_WIRE_133" : !hw.inout<i1>
        %10 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg name "_WHEN_WIRE_134" : !hw.inout<i1>
        %11 = sv.read_inout %19 : !hw.inout<i1>
        %20 = sv.reg name "_WHEN_WIRE_135" : !hw.inout<i1>
        %12 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg name "_WHEN_WIRE_136" : !hw.inout<i1>
        %13 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg name "_WHEN_WIRE_137" : !hw.inout<i1>
        %14 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg name "_WHEN_WIRE_138" : !hw.inout<i1>
        %15 = sv.read_inout %23 : !hw.inout<i1>
        %24 = sv.reg name "_WHEN_WIRE_139" : !hw.inout<i1>
        %16 = sv.read_inout %24 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %17, %0 : i1
                sv.bpassign %18, %1 : i1
                sv.bpassign %19, %2 : i1
                sv.bpassign %20, %2 : i1
                sv.bpassign %21, %2 : i1
                sv.bpassign %22, %2 : i1
                sv.bpassign %23, %2 : i1
                sv.bpassign %24, %2 : i1
            } else {
                sv.bpassign %17, %0 : i1
                sv.bpassign %18, %1 : i1
                sv.bpassign %19, %3 : i1
                sv.bpassign %20, %4 : i1
                sv.bpassign %21, %5 : i1
                sv.bpassign %22, %6 : i1
                sv.bpassign %23, %7 : i1
                sv.bpassign %24, %8 : i1
            }
        }
        %25 = comb.concat %16, %15, %14, %13, %12, %11, %10, %9 : i1, i1, i1, i1, i1, i1, i1, i1
        sv.verbatim "WHEN_ASSERT_277: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %9, %0) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_278: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %10, %1) : i1, i1, i1
        %26 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_279: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %11, %26) : i1, i1, i1
        %27 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_280: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %12, %27) : i1, i1, i1
        %28 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_281: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %13, %28) : i1, i1, i1
        %29 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_282: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %14, %29) : i1, i1, i1
        %30 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_283: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %15, %30) : i1, i1, i1
        %31 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_284: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %16, %31) : i1, i1, i1
        %33 = hw.constant -1 : i1
        %32 = comb.xor %33, %0 : i1
        sv.verbatim "WHEN_ASSERT_285: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %9, %0) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_286: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %10, %1) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_287: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %11, %3) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_288: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %12, %4) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_289: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %13, %5) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_290: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %14, %6) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_291: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %15, %7) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_292: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %16, %8) : i1, i1, i1
        hw.output %25 : i8
    }
    hw.module @Gen_unq1(%a: i8) -> (y: i8) {
        %0 = comb.extract %a from 0 : (i8) -> i1
        %1 = comb.extract %a from 1 : (i8) -> i1
        %2 = comb.extract %a from 2 : (i8) -> i1
        %3 = comb.extract %a from 3 : (i8) -> i1
        %4 = hw.constant 0 : i1
        %5 = comb.extract %a from 4 : (i8) -> i1
        %6 = comb.extract %a from 5 : (i8) -> i1
        %7 = comb.extract %a from 6 : (i8) -> i1
        %8 = comb.extract %a from 7 : (i8) -> i1
        %17 = sv.reg name "_WHEN_WIRE_140" : !hw.inout<i1>
        %9 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg name "_WHEN_WIRE_141" : !hw.inout<i1>
        %10 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg name "_WHEN_WIRE_142" : !hw.inout<i1>
        %11 = sv.read_inout %19 : !hw.inout<i1>
        %20 = sv.reg name "_WHEN_WIRE_143" : !hw.inout<i1>
        %12 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg name "_WHEN_WIRE_144" : !hw.inout<i1>
        %13 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg name "_WHEN_WIRE_145" : !hw.inout<i1>
        %14 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg name "_WHEN_WIRE_146" : !hw.inout<i1>
        %15 = sv.read_inout %23 : !hw.inout<i1>
        %24 = sv.reg name "_WHEN_WIRE_147" : !hw.inout<i1>
        %16 = sv.read_inout %24 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %17, %0 : i1
                sv.bpassign %18, %1 : i1
                sv.bpassign %19, %2 : i1
                sv.bpassign %20, %3 : i1
                sv.bpassign %21, %4 : i1
                sv.bpassign %22, %4 : i1
                sv.bpassign %23, %4 : i1
                sv.bpassign %24, %4 : i1
            } else {
                sv.bpassign %17, %0 : i1
                sv.bpassign %18, %1 : i1
                sv.bpassign %19, %2 : i1
                sv.bpassign %20, %3 : i1
                sv.bpassign %21, %5 : i1
                sv.bpassign %22, %6 : i1
                sv.bpassign %23, %7 : i1
                sv.bpassign %24, %8 : i1
            }
        }
        %25 = comb.concat %16, %15, %14, %13, %12, %11, %10, %9 : i1, i1, i1, i1, i1, i1, i1, i1
        sv.verbatim "WHEN_ASSERT_293: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %9, %0) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_294: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %10, %1) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_295: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %11, %2) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_296: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %12, %3) : i1, i1, i1
        %26 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_297: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %13, %26) : i1, i1, i1
        %27 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_298: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %14, %27) : i1, i1, i1
        %28 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_299: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %15, %28) : i1, i1, i1
        %29 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_300: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %16, %29) : i1, i1, i1
        %31 = hw.constant -1 : i1
        %30 = comb.xor %31, %0 : i1
        sv.verbatim "WHEN_ASSERT_301: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %9, %0) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_302: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %10, %1) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_303: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %11, %2) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_304: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %12, %3) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_305: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %13, %5) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_306: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %14, %6) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_307: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %15, %7) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_308: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %16, %8) : i1, i1, i1
        hw.output %25 : i8
    }
    hw.module @test_when_unique(%a: i8) -> (y: i8) {
        %0 = hw.instance "Gen_inst0" @Gen(a: %a: i8) -> (y: i8)
        %1 = hw.instance "Gen_inst1" @Gen_unq1(a: %a: i8) -> (y: i8)
        %2 = comb.or %0, %1 : i8
        hw.output %2 : i8
    }
}
