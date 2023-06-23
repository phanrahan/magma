module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_output_resolve(%I: i8, %x: i1) -> (O0: i8, O1: i2) {
        %1 = sv.wire sym @test_when_output_resolve.x name "x" : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %3 = hw.constant -1 : i8
        %2 = comb.xor %3, %0 : i8
        %5 = sv.reg name "_WHEN_WIRE_101" : !hw.inout<i8>
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
        %24 = comb.extract %4 from 1 : (i8) -> i1
        %25 = comb.extract %4 from 0 : (i8) -> i1
        %26 = comb.concat %25, %24 : i1, i1
        %27 = comb.extract %0 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_145: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %25, %27) : i1, i1, i1
        %28 = comb.extract %0 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_146: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %24, %28) : i1, i1, i1
        %29 = comb.extract %4 from 2 : (i8) -> i1
        %30 = comb.extract %0 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_147: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %29, %30) : i1, i1, i1
        %31 = comb.extract %4 from 3 : (i8) -> i1
        %32 = comb.extract %0 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_148: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %31, %32) : i1, i1, i1
        %33 = comb.extract %4 from 4 : (i8) -> i1
        %34 = comb.extract %0 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_149: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %33, %34) : i1, i1, i1
        %35 = comb.extract %4 from 5 : (i8) -> i1
        %36 = comb.extract %0 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_150: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %35, %36) : i1, i1, i1
        %37 = comb.extract %4 from 6 : (i8) -> i1
        %38 = comb.extract %0 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_151: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %37, %38) : i1, i1, i1
        %39 = comb.extract %4 from 7 : (i8) -> i1
        %40 = comb.extract %0 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_152: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%x, %39, %40) : i1, i1, i1
        %42 = hw.constant -1 : i1
        %41 = comb.xor %42, %x : i1
        %43 = comb.extract %2 from 0 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_153: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %25, %43) : i1, i1, i1
        %44 = comb.extract %2 from 1 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_154: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %24, %44) : i1, i1, i1
        %45 = comb.extract %2 from 2 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_155: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %29, %45) : i1, i1, i1
        %46 = comb.extract %2 from 3 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_156: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %31, %46) : i1, i1, i1
        %47 = comb.extract %2 from 4 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_157: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %33, %47) : i1, i1, i1
        %48 = comb.extract %2 from 5 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_158: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %35, %48) : i1, i1, i1
        %49 = comb.extract %2 from 6 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_159: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %37, %49) : i1, i1, i1
        %50 = comb.extract %2 from 7 : (i8) -> i1
        sv.verbatim "WHEN_ASSERT_160: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %39, %50) : i1, i1, i1
        hw.output %4, %26 : i8, i2
    }
}
