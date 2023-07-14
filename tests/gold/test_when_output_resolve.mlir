module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_output_resolve(%I: i8, %x: i1) -> (O0: i8, O1: i2) {
        %1 = sv.wire sym @test_when_output_resolve.x name "x" : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %3 = hw.constant -1 : i8
        %2 = comb.xor %3, %0 : i8
        %5 = sv.reg : !hw.inout<i8>
        %4 = sv.read_inout %5 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %x {
                %14 = comb.concat %13, %12, %11, %10, %9, %8, %7, %6 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %5, %14 : i8
            } else {
                %23 = comb.concat %22, %21, %20, %19, %18, %17, %16, %15 : i1, i1, i1, i1, i1, i1, i1, i1
                sv.bpassign %5, %23 : i8
            }
        }
        %6 = comb.extract %0 from 0 : (i8) -> i1
        %7 = comb.extract %0 from 1 : (i8) -> i1
        %8 = comb.extract %0 from 2 : (i8) -> i1
        %9 = comb.extract %0 from 3 : (i8) -> i1
        %10 = comb.extract %0 from 4 : (i8) -> i1
        %11 = comb.extract %0 from 5 : (i8) -> i1
        %12 = comb.extract %0 from 6 : (i8) -> i1
        %13 = comb.extract %0 from 7 : (i8) -> i1
        %15 = comb.extract %2 from 0 : (i8) -> i1
        %16 = comb.extract %2 from 1 : (i8) -> i1
        %17 = comb.extract %2 from 2 : (i8) -> i1
        %18 = comb.extract %2 from 3 : (i8) -> i1
        %19 = comb.extract %2 from 4 : (i8) -> i1
        %20 = comb.extract %2 from 5 : (i8) -> i1
        %21 = comb.extract %2 from 6 : (i8) -> i1
        %22 = comb.extract %2 from 7 : (i8) -> i1
        %24 = comb.extract %4 from 0 : (i8) -> i1
        %26 = sv.wire sym @test_when_output_resolve._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %26, %24 : i1
        %25 = sv.read_inout %26 : !hw.inout<i1>
        %27 = comb.extract %4 from 1 : (i8) -> i1
        %29 = sv.wire sym @test_when_output_resolve._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %29, %27 : i1
        %28 = sv.read_inout %29 : !hw.inout<i1>
        %30 = comb.extract %4 from 2 : (i8) -> i1
        %32 = sv.wire sym @test_when_output_resolve._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %32, %30 : i1
        %31 = sv.read_inout %32 : !hw.inout<i1>
        %33 = comb.extract %4 from 3 : (i8) -> i1
        %35 = sv.wire sym @test_when_output_resolve._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %35, %33 : i1
        %34 = sv.read_inout %35 : !hw.inout<i1>
        %36 = comb.extract %4 from 4 : (i8) -> i1
        %38 = sv.wire sym @test_when_output_resolve._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %38, %36 : i1
        %37 = sv.read_inout %38 : !hw.inout<i1>
        %39 = comb.extract %4 from 5 : (i8) -> i1
        %41 = sv.wire sym @test_when_output_resolve._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i1>
        sv.assign %41, %39 : i1
        %40 = sv.read_inout %41 : !hw.inout<i1>
        %42 = comb.extract %4 from 6 : (i8) -> i1
        %44 = sv.wire sym @test_when_output_resolve._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i1>
        sv.assign %44, %42 : i1
        %43 = sv.read_inout %44 : !hw.inout<i1>
        %45 = comb.extract %4 from 7 : (i8) -> i1
        %47 = sv.wire sym @test_when_output_resolve._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i1>
        sv.assign %47, %45 : i1
        %46 = sv.read_inout %47 : !hw.inout<i1>
        %48 = comb.concat %46, %43, %40, %37, %34, %31, %28, %25 : i1, i1, i1, i1, i1, i1, i1, i1
        %49 = comb.concat %25, %28 : i1, i1
        %50 = comb.extract %0 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %25, %50) : i1, i1, i1
        %51 = comb.extract %0 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %28, %51) : i1, i1, i1
        %52 = comb.extract %0 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %31, %52) : i1, i1, i1
        %53 = comb.extract %0 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %34, %53) : i1, i1, i1
        %54 = comb.extract %0 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %37, %54) : i1, i1, i1
        %55 = comb.extract %0 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %40, %55) : i1, i1, i1
        %56 = comb.extract %0 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %43, %56) : i1, i1, i1
        %57 = comb.extract %0 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %46, %57) : i1, i1, i1
        %59 = hw.constant -1 : i1
        %58 = comb.xor %59, %x : i1
        %60 = comb.extract %2 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%58, %25, %60) : i1, i1, i1
        %61 = comb.extract %2 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%58, %28, %61) : i1, i1, i1
        %62 = comb.extract %2 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%58, %31, %62) : i1, i1, i1
        %63 = comb.extract %2 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%58, %34, %63) : i1, i1, i1
        %64 = comb.extract %2 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%58, %37, %64) : i1, i1, i1
        %65 = comb.extract %2 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%58, %40, %65) : i1, i1, i1
        %66 = comb.extract %2 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%58, %43, %66) : i1, i1, i1
        %67 = comb.extract %2 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%58, %46, %67) : i1, i1, i1
        hw.output %48, %49 : i8, i2
    }
}
