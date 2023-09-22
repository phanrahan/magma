module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_array_resolved_after(%I: i8, %S: i1) -> (O: i16) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 0 : i1
        %2 = hw.constant 0 : i1
        %3 = hw.constant 0 : i1
        %4 = hw.constant 0 : i1
        %5 = hw.constant 0 : i1
        %6 = hw.constant 0 : i1
        %7 = hw.constant 0 : i1
        %9 = hw.constant -1 : i8
        %8 = comb.xor %9, %I : i8
        %11 = sv.reg : !hw.inout<i8>
        %10 = sv.read_inout %11 : !hw.inout<i8>
        sv.alwayscomb {
            %20 = comb.concat %19, %18, %17, %16, %15, %14, %13, %12 : i1, i1, i1, i1, i1, i1, i1, i1
            sv.bpassign %11, %20 : i8
            sv.if %S {
                %29 = comb.concat %28, %27, %26, %25, %24, %23, %22, %21 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %11, %29 : i8
            }
        }
        %12 = comb.extract %8 from 0 : (i8) -> i1
        %13 = comb.extract %8 from 1 : (i8) -> i1
        %14 = comb.extract %8 from 2 : (i8) -> i1
        %15 = comb.extract %8 from 3 : (i8) -> i1
        %16 = comb.extract %8 from 4 : (i8) -> i1
        %17 = comb.extract %8 from 5 : (i8) -> i1
        %18 = comb.extract %8 from 6 : (i8) -> i1
        %19 = comb.extract %8 from 7 : (i8) -> i1
        %21 = comb.extract %I from 0 : (i8) -> i1
        %22 = comb.extract %I from 1 : (i8) -> i1
        %23 = comb.extract %I from 2 : (i8) -> i1
        %24 = comb.extract %I from 3 : (i8) -> i1
        %25 = comb.extract %I from 4 : (i8) -> i1
        %26 = comb.extract %I from 5 : (i8) -> i1
        %27 = comb.extract %I from 6 : (i8) -> i1
        %28 = comb.extract %I from 7 : (i8) -> i1
        %30 = comb.extract %10 from 0 : (i8) -> i1
        %32 = sv.wire sym @test_when_array_resolved_after._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %32, %30 : i1
        %31 = sv.read_inout %32 : !hw.inout<i1>
        %33 = comb.extract %10 from 1 : (i8) -> i1
        %35 = sv.wire sym @test_when_array_resolved_after._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %35, %33 : i1
        %34 = sv.read_inout %35 : !hw.inout<i1>
        %36 = comb.extract %10 from 2 : (i8) -> i1
        %38 = sv.wire sym @test_when_array_resolved_after._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %38, %36 : i1
        %37 = sv.read_inout %38 : !hw.inout<i1>
        %39 = comb.extract %10 from 3 : (i8) -> i1
        %41 = sv.wire sym @test_when_array_resolved_after._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %41, %39 : i1
        %40 = sv.read_inout %41 : !hw.inout<i1>
        %42 = comb.extract %10 from 4 : (i8) -> i1
        %44 = sv.wire sym @test_when_array_resolved_after._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %44, %42 : i1
        %43 = sv.read_inout %44 : !hw.inout<i1>
        %45 = comb.extract %10 from 5 : (i8) -> i1
        %47 = sv.wire sym @test_when_array_resolved_after._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i1>
        sv.assign %47, %45 : i1
        %46 = sv.read_inout %47 : !hw.inout<i1>
        %48 = comb.extract %10 from 6 : (i8) -> i1
        %50 = sv.wire sym @test_when_array_resolved_after._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i1>
        sv.assign %50, %48 : i1
        %49 = sv.read_inout %50 : !hw.inout<i1>
        %51 = comb.extract %10 from 7 : (i8) -> i1
        %53 = sv.wire sym @test_when_array_resolved_after._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i1>
        sv.assign %53, %51 : i1
        %52 = sv.read_inout %53 : !hw.inout<i1>
        %54 = comb.concat %52, %49, %46, %43, %40, %37, %34, %31, %7, %6, %5, %4, %3, %2, %1, %0 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %55 = comb.extract %I from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %31, %55) : i1, i1, i1
        %56 = comb.extract %I from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %34, %56) : i1, i1, i1
        %57 = comb.extract %I from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %37, %57) : i1, i1, i1
        %58 = comb.extract %I from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %40, %58) : i1, i1, i1
        %59 = comb.extract %I from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %43, %59) : i1, i1, i1
        %60 = comb.extract %I from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %46, %60) : i1, i1, i1
        %61 = comb.extract %I from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %49, %61) : i1, i1, i1
        %62 = comb.extract %I from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %52, %62) : i1, i1, i1
        %64 = hw.constant -1 : i1
        %63 = comb.xor %64, %S : i1
        %65 = comb.extract %8 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%63, %31, %65) : i1, i1, i1
        %66 = comb.xor %64, %S : i1
        %67 = comb.extract %8 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%66, %34, %67) : i1, i1, i1
        %68 = comb.xor %64, %S : i1
        %69 = comb.extract %8 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%68, %37, %69) : i1, i1, i1
        %70 = comb.xor %64, %S : i1
        %71 = comb.extract %8 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%70, %40, %71) : i1, i1, i1
        %72 = comb.xor %64, %S : i1
        %73 = comb.extract %8 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%72, %43, %73) : i1, i1, i1
        %74 = comb.xor %64, %S : i1
        %75 = comb.extract %8 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%74, %46, %75) : i1, i1, i1
        %76 = comb.xor %64, %S : i1
        %77 = comb.extract %8 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%76, %49, %77) : i1, i1, i1
        %78 = comb.xor %64, %S : i1
        %79 = comb.extract %8 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%78, %52, %79) : i1, i1, i1
        hw.output %54 : i16
    }
}
