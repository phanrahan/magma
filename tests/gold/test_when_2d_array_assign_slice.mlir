module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_2d_array_assign_slice(in %I: !hw.array<4xi2>, in %S: i1, out O: !hw.array<4xi2>) {
        %1 = sv.reg : !hw.inout<!hw.array<4xi2>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<4xi2>>
        sv.alwayscomb {
            sv.if %S {
                %10 = hw.array_create %5, %3, %9, %7 : i2
                sv.bpassign %1, %10 : !hw.array<4xi2>
            } else {
                %11 = hw.array_create %9, %7, %5, %3 : i2
                sv.bpassign %1, %11 : !hw.array<4xi2>
            }
        }
        %2 = hw.constant 2 : i2
        %3 = hw.array_get %I[%2] : !hw.array<4xi2>, i2
        %4 = hw.constant 3 : i2
        %5 = hw.array_get %I[%4] : !hw.array<4xi2>, i2
        %6 = hw.constant 0 : i2
        %7 = hw.array_get %I[%6] : !hw.array<4xi2>, i2
        %8 = hw.constant 1 : i2
        %9 = hw.array_get %I[%8] : !hw.array<4xi2>, i2
        %12 = hw.array_get %0[%6] : !hw.array<4xi2>, i2
        %14 = sv.wire sym @test_when_2d_array_assign_slice._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i2>
        sv.assign %14, %12 : i2
        %13 = sv.read_inout %14 : !hw.inout<i2>
        %15 = hw.array_get %0[%8] : !hw.array<4xi2>, i2
        %17 = sv.wire sym @test_when_2d_array_assign_slice._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i2>
        sv.assign %17, %15 : i2
        %16 = sv.read_inout %17 : !hw.inout<i2>
        %18 = hw.array_get %0[%2] : !hw.array<4xi2>, i2
        %20 = sv.wire sym @test_when_2d_array_assign_slice._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i2>
        sv.assign %20, %18 : i2
        %19 = sv.read_inout %20 : !hw.inout<i2>
        %21 = hw.array_get %0[%4] : !hw.array<4xi2>, i2
        %23 = sv.wire sym @test_when_2d_array_assign_slice._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i2>
        sv.assign %23, %21 : i2
        %22 = sv.read_inout %23 : !hw.inout<i2>
        %24 = hw.array_create %22, %19, %16, %13 : i2
        %25 = hw.array_create %16, %13 : i2
        %27 = sv.wire sym @test_when_2d_array_assign_slice._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<!hw.array<2xi2>>
        sv.assign %27, %25 : !hw.array<2xi2>
        %26 = sv.read_inout %27 : !hw.inout<!hw.array<2xi2>>
        %29 = hw.constant 1 : i1
        %28 = hw.array_get %26[%29] : !hw.array<2xi2>, i1
        %31 = hw.constant 0 : i1
        %30 = hw.array_get %26[%31] : !hw.array<2xi2>, i1
        %32 = hw.array_get %I[%8] : !hw.array<4xi2>, i2
        %33 = hw.array_get %I[%6] : !hw.array<4xi2>, i2
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%S, %28, %30, %32, %33) : i1, i2, i2, i2, i2
        %34 = hw.array_get %I[%2] : !hw.array<4xi2>, i2
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %19, %34) : i1, i2, i2
        %35 = hw.array_get %I[%4] : !hw.array<4xi2>, i2
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %22, %35) : i1, i2, i2
        %37 = hw.constant -1 : i1
        %36 = comb.xor %37, %S : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%36, %19, %33) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%36, %22, %32) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%36, %13, %34) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%36, %16, %35) : i1, i2, i2
        hw.output %24 : !hw.array<4xi2>
    }
}
