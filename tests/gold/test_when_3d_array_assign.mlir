module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_3d_array_assign(in %I: !hw.array<2x!hw.array<2xi2>>, in %S: i1, out O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = sv.reg : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %11 = hw.array_create %9, %8 : i2
                %12 = hw.array_create %6, %5 : i2
                %10 = hw.array_create %12, %11 : !hw.array<2xi2>
                sv.bpassign %1, %10 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %14 = hw.array_create %5, %6 : i2
                %15 = hw.array_create %8, %9 : i2
                %13 = hw.array_create %15, %14 : !hw.array<2xi2>
                sv.bpassign %1, %13 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        %2 = hw.constant 1 : i1
        %3 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %4 = hw.constant 0 : i1
        %5 = hw.array_get %3[%4] : !hw.array<2xi2>, i1
        %6 = hw.array_get %3[%2] : !hw.array<2xi2>, i1
        %7 = hw.array_get %I[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %8 = hw.array_get %7[%4] : !hw.array<2xi2>, i1
        %9 = hw.array_get %7[%2] : !hw.array<2xi2>, i1
        %16 = hw.array_get %0[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %17 = hw.array_get %16[%4] : !hw.array<2xi2>, i1
        %19 = sv.wire sym @test_when_3d_array_assign._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i2>
        sv.assign %19, %17 : i2
        %18 = sv.read_inout %19 : !hw.inout<i2>
        %20 = hw.array_get %16[%2] : !hw.array<2xi2>, i1
        %22 = sv.wire sym @test_when_3d_array_assign._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i2>
        sv.assign %22, %20 : i2
        %21 = sv.read_inout %22 : !hw.inout<i2>
        %23 = hw.array_create %21, %18 : i2
        %24 = hw.array_get %0[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %25 = hw.array_get %24[%4] : !hw.array<2xi2>, i1
        %27 = sv.wire sym @test_when_3d_array_assign._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i2>
        sv.assign %27, %25 : i2
        %26 = sv.read_inout %27 : !hw.inout<i2>
        %28 = hw.array_get %24[%2] : !hw.array<2xi2>, i1
        %30 = sv.wire sym @test_when_3d_array_assign._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i2>
        sv.assign %30, %28 : i2
        %29 = sv.read_inout %30 : !hw.inout<i2>
        %31 = hw.array_create %29, %26 : i2
        %32 = hw.array_create %31, %23 : !hw.array<2xi2>
        %33 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %34 = hw.array_get %33[%4] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %26, %34) : i1, i2, i2
        %35 = hw.array_get %33[%2] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %29, %35) : i1, i2, i2
        %36 = hw.array_get %I[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %37 = hw.array_get %36[%4] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %18, %37) : i1, i2, i2
        %38 = hw.array_get %36[%2] : !hw.array<2xi2>, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %21, %38) : i1, i2, i2
        %40 = hw.constant -1 : i1
        %39 = comb.xor %40, %S : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%39, %26, %38) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%39, %29, %37) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%39, %18, %35) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%39, %21, %34) : i1, i2, i2
        hw.output %32 : !hw.array<2x!hw.array<2xi2>>
    }
}
