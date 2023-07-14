module attributes {circt.loweringOptions = "locationInfoStyle=none,disallowLocalVariables"} {
    hw.module @test_when_temporary_resolved(%I: i8, %S: i2, %CLK: i1) -> (O: i8) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %2 = comb.extract %1 from 1 : (i8) -> i1
        %4 = sv.wire sym @test_when_temporary_resolved._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %4, %2 : i1
        %3 = sv.read_inout %4 : !hw.inout<i1>
        %5 = comb.extract %1 from 2 : (i8) -> i1
        %7 = sv.wire sym @test_when_temporary_resolved._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %7, %5 : i1
        %6 = sv.read_inout %7 : !hw.inout<i1>
        %8 = comb.extract %1 from 3 : (i8) -> i1
        %10 = sv.wire sym @test_when_temporary_resolved._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %10, %8 : i1
        %9 = sv.read_inout %10 : !hw.inout<i1>
        %11 = comb.extract %1 from 4 : (i8) -> i1
        %13 = sv.wire sym @test_when_temporary_resolved._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %13, %11 : i1
        %12 = sv.read_inout %13 : !hw.inout<i1>
        %14 = comb.extract %1 from 5 : (i8) -> i1
        %16 = sv.wire sym @test_when_temporary_resolved._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i1>
        sv.assign %16, %14 : i1
        %15 = sv.read_inout %16 : !hw.inout<i1>
        %17 = comb.extract %1 from 6 : (i8) -> i1
        %19 = sv.wire sym @test_when_temporary_resolved._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i1>
        sv.assign %19, %17 : i1
        %18 = sv.read_inout %19 : !hw.inout<i1>
        %20 = comb.extract %1 from 7 : (i8) -> i1
        %22 = sv.wire sym @test_when_temporary_resolved._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i1>
        sv.assign %22, %20 : i1
        %21 = sv.read_inout %22 : !hw.inout<i1>
        %24 = comb.concat %21, %18, %15, %12, %9, %6, %3, %23 : i1, i1, i1, i1, i1, i1, i1, i1
        %26 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %26, %24 : i8
        }
        %27 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %26, %27 : i8
        }
        %25 = sv.read_inout %26 : !hw.inout<i8>
        %28 = hw.constant 4 : i8
        %29 = comb.sub %25, %28 : i8
        %30 = comb.extract %S from 1 : (i2) -> i1
        %31 = comb.extract %25 from 0 : (i8) -> i1
        %32 = comb.extract %25 from 1 : (i8) -> i1
        %33 = comb.extract %25 from 2 : (i8) -> i1
        %34 = comb.extract %25 from 3 : (i8) -> i1
        %35 = comb.extract %25 from 4 : (i8) -> i1
        %36 = comb.extract %25 from 5 : (i8) -> i1
        %37 = comb.extract %25 from 6 : (i8) -> i1
        %38 = comb.extract %25 from 7 : (i8) -> i1
        %39 = hw.constant 0 : i1
        %40 = comb.concat %39, %38, %37, %36, %35, %34, %33, %32, %31 : i1, i1, i1, i1, i1, i1, i1, i1, i1
        %41 = comb.extract %I from 0 : (i8) -> i1
        %42 = comb.extract %I from 1 : (i8) -> i1
        %43 = comb.extract %I from 2 : (i8) -> i1
        %44 = comb.extract %I from 3 : (i8) -> i1
        %45 = comb.extract %I from 4 : (i8) -> i1
        %46 = comb.extract %I from 5 : (i8) -> i1
        %47 = comb.extract %I from 6 : (i8) -> i1
        %48 = comb.extract %I from 7 : (i8) -> i1
        %49 = hw.constant 0 : i1
        %50 = comb.concat %49, %48, %47, %46, %45, %44, %43, %42, %41 : i1, i1, i1, i1, i1, i1, i1, i1, i1
        %51 = comb.add %40, %50 : i9
        %52 = comb.extract %51 from 0 : (i9) -> i1
        %53 = comb.extract %51 from 1 : (i9) -> i1
        %54 = comb.extract %51 from 2 : (i9) -> i1
        %55 = comb.extract %51 from 3 : (i9) -> i1
        %56 = comb.extract %51 from 4 : (i9) -> i1
        %57 = comb.extract %51 from 5 : (i9) -> i1
        %58 = comb.extract %51 from 6 : (i9) -> i1
        %59 = comb.extract %51 from 7 : (i9) -> i1
        %60 = comb.concat %59, %58, %57, %56, %55, %54, %53, %52 : i1, i1, i1, i1, i1, i1, i1, i1
        %61 = comb.concat %59, %58, %57, %56, %55, %54, %53, %52 : i1, i1, i1, i1, i1, i1, i1, i1
        %62 = hw.constant 4 : i8
        %63 = comb.sub %61, %62 : i8
        %64 = sv.reg : !hw.inout<i8>
        %1 = sv.read_inout %64 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %0 {
                %73 = comb.concat %72, %71, %70, %69, %68, %67, %66, %65 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %64, %73 : i8
            } else {
                sv.if %30 {
                    %74 = comb.concat %59, %58, %57, %56, %55, %54, %53, %52 : i1, i1, i1, i1, i1, i1, i1, i1
                    sv.bpassign %64, %74 : i8
                } else {
                    %83 = comb.concat %82, %81, %80, %79, %78, %77, %76, %75 : i1, i1, i1, i1, i1, i1, i1, i1
                    sv.bpassign %64, %83 : i8
                }
            }
        }
        %65 = comb.extract %29 from 0 : (i8) -> i1
        %66 = comb.extract %29 from 1 : (i8) -> i1
        %67 = comb.extract %29 from 2 : (i8) -> i1
        %68 = comb.extract %29 from 3 : (i8) -> i1
        %69 = comb.extract %29 from 4 : (i8) -> i1
        %70 = comb.extract %29 from 5 : (i8) -> i1
        %71 = comb.extract %29 from 6 : (i8) -> i1
        %72 = comb.extract %29 from 7 : (i8) -> i1
        %75 = comb.extract %63 from 0 : (i8) -> i1
        %76 = comb.extract %63 from 1 : (i8) -> i1
        %77 = comb.extract %63 from 2 : (i8) -> i1
        %78 = comb.extract %63 from 3 : (i8) -> i1
        %79 = comb.extract %63 from 4 : (i8) -> i1
        %80 = comb.extract %63 from 5 : (i8) -> i1
        %81 = comb.extract %63 from 6 : (i8) -> i1
        %82 = comb.extract %63 from 7 : (i8) -> i1
        %84 = comb.extract %1 from 0 : (i8) -> i1
        %85 = sv.wire sym @test_when_temporary_resolved._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %85, %84 : i1
        %23 = sv.read_inout %85 : !hw.inout<i1>
        %86 = comb.concat %21, %18, %15, %12, %9, %6, %3, %23 : i1, i1, i1, i1, i1, i1, i1, i1
        %87 = comb.extract %29 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %23, %87) : i1, i1, i1
        %88 = comb.extract %29 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %3, %88) : i1, i1, i1
        %89 = comb.extract %29 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %6, %89) : i1, i1, i1
        %90 = comb.extract %29 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %9, %90) : i1, i1, i1
        %91 = comb.extract %29 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %12, %91) : i1, i1, i1
        %92 = comb.extract %29 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %15, %92) : i1, i1, i1
        %93 = comb.extract %29 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %18, %93) : i1, i1, i1
        %94 = comb.extract %29 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %21, %94) : i1, i1, i1
        %96 = hw.constant -1 : i1
        %95 = comb.xor %96, %0 : i1
        %97 = comb.and %95, %30 : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%97, %23, %52) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%97, %3, %53) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%97, %6, %54) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%97, %9, %55) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%97, %12, %56) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%97, %15, %57) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%97, %18, %58) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%97, %21, %59) : i1, i1, i1
        %98 = comb.xor %96, %30 : i1
        %99 = comb.and %95, %98 : i1
        %100 = comb.extract %63 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%99, %23, %100) : i1, i1, i1
        %101 = comb.extract %63 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%99, %3, %101) : i1, i1, i1
        %102 = comb.extract %63 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_18: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%99, %6, %102) : i1, i1, i1
        %103 = comb.extract %63 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_19: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%99, %9, %103) : i1, i1, i1
        %104 = comb.extract %63 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_20: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%99, %12, %104) : i1, i1, i1
        %105 = comb.extract %63 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_21: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%99, %15, %105) : i1, i1, i1
        %106 = comb.extract %63 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_22: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%99, %18, %106) : i1, i1, i1
        %107 = comb.extract %63 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_23: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%99, %21, %107) : i1, i1, i1
        hw.output %86 : i8
    }
}
