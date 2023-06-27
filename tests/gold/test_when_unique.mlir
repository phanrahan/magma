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
        %17 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i1>
        %9 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %10 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg name "_WHEN_WIRE_2" : !hw.inout<i1>
        %11 = sv.read_inout %19 : !hw.inout<i1>
        %20 = sv.reg name "_WHEN_WIRE_3" : !hw.inout<i1>
        %12 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg name "_WHEN_WIRE_4" : !hw.inout<i1>
        %13 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg name "_WHEN_WIRE_5" : !hw.inout<i1>
        %14 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg name "_WHEN_WIRE_6" : !hw.inout<i1>
        %15 = sv.read_inout %23 : !hw.inout<i1>
        %24 = sv.reg name "_WHEN_WIRE_7" : !hw.inout<i1>
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
        sv.verbatim "WHEN_ASSERT_334: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %9, %0) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_335: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %10, %1) : i1, i1, i1
        %26 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_336: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %11, %26) : i1, i1, i1
        %27 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_337: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %12, %27) : i1, i1, i1
        %28 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_338: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %13, %28) : i1, i1, i1
        %29 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_339: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %14, %29) : i1, i1, i1
        %30 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_340: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %15, %30) : i1, i1, i1
        %31 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_341: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %16, %31) : i1, i1, i1
        %33 = hw.constant -1 : i1
        %32 = comb.xor %33, %0 : i1
        sv.verbatim "WHEN_ASSERT_342: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %9, %0) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_343: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %10, %1) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_344: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %11, %3) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_345: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %12, %4) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_346: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %13, %5) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_347: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %14, %6) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_348: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %15, %7) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_349: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %16, %8) : i1, i1, i1
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
        %17 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i1>
        %9 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %10 = sv.read_inout %18 : !hw.inout<i1>
        %19 = sv.reg name "_WHEN_WIRE_2" : !hw.inout<i1>
        %11 = sv.read_inout %19 : !hw.inout<i1>
        %20 = sv.reg name "_WHEN_WIRE_3" : !hw.inout<i1>
        %12 = sv.read_inout %20 : !hw.inout<i1>
        %21 = sv.reg name "_WHEN_WIRE_4" : !hw.inout<i1>
        %13 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg name "_WHEN_WIRE_5" : !hw.inout<i1>
        %14 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg name "_WHEN_WIRE_6" : !hw.inout<i1>
        %15 = sv.read_inout %23 : !hw.inout<i1>
        %24 = sv.reg name "_WHEN_WIRE_7" : !hw.inout<i1>
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
        sv.verbatim "WHEN_ASSERT_350: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %9, %0) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_351: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %10, %1) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_352: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %11, %2) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_353: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %12, %3) : i1, i1, i1
        %26 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_354: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %13, %26) : i1, i1, i1
        %27 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_355: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %14, %27) : i1, i1, i1
        %28 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_356: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %15, %28) : i1, i1, i1
        %29 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_357: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %16, %29) : i1, i1, i1
        %31 = hw.constant -1 : i1
        %30 = comb.xor %31, %0 : i1
        sv.verbatim "WHEN_ASSERT_358: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %9, %0) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_359: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %10, %1) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_360: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %11, %2) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_361: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %12, %3) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_362: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %13, %5) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_363: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %14, %6) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_364: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %15, %7) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_365: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %16, %8) : i1, i1, i1
        hw.output %25 : i8
    }
    hw.module @test_when_unique(%a: i8) -> (y: i8) {
        %0 = hw.instance "Gen_inst0" @Gen(a: %a: i8) -> (y: i8)
        %1 = hw.instance "Gen_inst1" @Gen_unq1(a: %a: i8) -> (y: i8)
        %2 = comb.or %0, %1 : i8
        hw.output %2 : i8
    }
}
