module attributes {circt.loweringOptions = "locationInfoStyle=none,disallowLocalVariables"} {
    hw.module @test_when_temporary_resolved(%I: i8, %S: i2, %CLK: i1) -> (O: i8) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %3 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %1 : i8
        }
        %4 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %3, %4 : i8
        }
        %2 = sv.read_inout %3 : !hw.inout<i8>
        %5 = hw.constant 4 : i8
        %6 = comb.sub %2, %5 : i8
        %7 = comb.extract %S from 1 : (i2) -> i1
        %8 = comb.extract %2 from 0 : (i8) -> i1
        %9 = comb.extract %2 from 1 : (i8) -> i1
        %10 = comb.extract %2 from 2 : (i8) -> i1
        %11 = comb.extract %2 from 3 : (i8) -> i1
        %12 = comb.extract %2 from 4 : (i8) -> i1
        %13 = comb.extract %2 from 5 : (i8) -> i1
        %14 = comb.extract %2 from 6 : (i8) -> i1
        %15 = comb.extract %2 from 7 : (i8) -> i1
        %16 = hw.constant 0 : i1
        %17 = comb.concat %16, %15, %14, %13, %12, %11, %10, %9, %8 : i1, i1, i1, i1, i1, i1, i1, i1, i1
        %18 = comb.extract %I from 0 : (i8) -> i1
        %19 = comb.extract %I from 1 : (i8) -> i1
        %20 = comb.extract %I from 2 : (i8) -> i1
        %21 = comb.extract %I from 3 : (i8) -> i1
        %22 = comb.extract %I from 4 : (i8) -> i1
        %23 = comb.extract %I from 5 : (i8) -> i1
        %24 = comb.extract %I from 6 : (i8) -> i1
        %25 = comb.extract %I from 7 : (i8) -> i1
        %26 = hw.constant 0 : i1
        %27 = comb.concat %26, %25, %24, %23, %22, %21, %20, %19, %18 : i1, i1, i1, i1, i1, i1, i1, i1, i1
        %28 = comb.add %17, %27 : i9
        %29 = comb.extract %28 from 0 : (i9) -> i1
        %30 = comb.extract %28 from 1 : (i9) -> i1
        %31 = comb.extract %28 from 2 : (i9) -> i1
        %32 = comb.extract %28 from 3 : (i9) -> i1
        %33 = comb.extract %28 from 4 : (i9) -> i1
        %34 = comb.extract %28 from 5 : (i9) -> i1
        %35 = comb.extract %28 from 6 : (i9) -> i1
        %36 = comb.extract %28 from 7 : (i9) -> i1
        %37 = comb.concat %36, %35, %34, %33, %32, %31, %30, %29 : i1, i1, i1, i1, i1, i1, i1, i1
        %38 = comb.concat %36, %35, %34, %33, %32, %31, %30, %29 : i1, i1, i1, i1, i1, i1, i1, i1
        %39 = hw.constant 4 : i8
        %40 = comb.sub %38, %39 : i8
        %41 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i8>
        %1 = sv.read_inout %41 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %0 {
                %50 = comb.concat %49, %48, %47, %46, %45, %44, %43, %42 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %41, %50 : i8
            } else {
                sv.if %7 {
                    %51 = comb.concat %36, %35, %34, %33, %32, %31, %30, %29 : i1, i1, i1, i1, i1, i1, i1, i1
                    sv.bpassign %41, %51 : i8
                } else {
                    %60 = comb.concat %59, %58, %57, %56, %55, %54, %53, %52 : i1, i1, i1, i1, i1, i1, i1, i1
                    sv.bpassign %41, %60 : i8
                }
            }
        }
        %42 = comb.extract %6 from 0 : (i8) -> i1
        %43 = comb.extract %6 from 1 : (i8) -> i1
        %44 = comb.extract %6 from 2 : (i8) -> i1
        %45 = comb.extract %6 from 3 : (i8) -> i1
        %46 = comb.extract %6 from 4 : (i8) -> i1
        %47 = comb.extract %6 from 5 : (i8) -> i1
        %48 = comb.extract %6 from 6 : (i8) -> i1
        %49 = comb.extract %6 from 7 : (i8) -> i1
        %52 = comb.extract %40 from 0 : (i8) -> i1
        %53 = comb.extract %40 from 1 : (i8) -> i1
        %54 = comb.extract %40 from 2 : (i8) -> i1
        %55 = comb.extract %40 from 3 : (i8) -> i1
        %56 = comb.extract %40 from 4 : (i8) -> i1
        %57 = comb.extract %40 from 5 : (i8) -> i1
        %58 = comb.extract %40 from 6 : (i8) -> i1
        %59 = comb.extract %40 from 7 : (i8) -> i1
        %61 = comb.extract %1 from 0 : (i8) -> i1
        %62 = comb.extract %6 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %61, %62) : i1, i1, i1
        %63 = comb.extract %1 from 1 : (i8) -> i1
        %64 = comb.extract %6 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %63, %64) : i1, i1, i1
        %65 = comb.extract %1 from 2 : (i8) -> i1
        %66 = comb.extract %6 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %65, %66) : i1, i1, i1
        %67 = comb.extract %1 from 3 : (i8) -> i1
        %68 = comb.extract %6 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %67, %68) : i1, i1, i1
        %69 = comb.extract %1 from 4 : (i8) -> i1
        %70 = comb.extract %6 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %69, %70) : i1, i1, i1
        %71 = comb.extract %1 from 5 : (i8) -> i1
        %72 = comb.extract %6 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %71, %72) : i1, i1, i1
        %73 = comb.extract %1 from 6 : (i8) -> i1
        %74 = comb.extract %6 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %73, %74) : i1, i1, i1
        %75 = comb.extract %1 from 7 : (i8) -> i1
        %76 = comb.extract %6 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %75, %76) : i1, i1, i1
        %78 = hw.constant -1 : i1
        %77 = comb.xor %78, %0 : i1
        %79 = comb.and %77, %7 : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%79, %61, %29) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%79, %63, %30) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%79, %65, %31) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%79, %67, %32) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%79, %69, %33) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%79, %71, %34) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%79, %73, %35) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%79, %75, %36) : i1, i1, i1
        %80 = comb.xor %78, %7 : i1
        %81 = comb.and %77, %80 : i1
        %82 = comb.extract %40 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%81, %61, %82) : i1, i1, i1
        %83 = comb.extract %40 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%81, %63, %83) : i1, i1, i1
        %84 = comb.extract %40 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_18: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%81, %65, %84) : i1, i1, i1
        %85 = comb.extract %40 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_19: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%81, %67, %85) : i1, i1, i1
        %86 = comb.extract %40 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_20: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%81, %69, %86) : i1, i1, i1
        %87 = comb.extract %40 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_21: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%81, %71, %87) : i1, i1, i1
        %88 = comb.extract %40 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_22: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%81, %73, %88) : i1, i1, i1
        %89 = comb.extract %40 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_23: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%81, %75, %89) : i1, i1, i1
        hw.output %1 : i8
    }
}
