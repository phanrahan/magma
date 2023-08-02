module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_False(%I: !hw.array<2x!hw.array<2x!hw.struct<x: i1, y: i2>>>, %S: i1) -> (O: !hw.array<2x!hw.struct<x: i1, y: i2>>) {
        %1 = hw.constant 1 : i1
        %0 = hw.array_get %I[%1] : !hw.array<2x!hw.array<2x!hw.struct<x: i1, y: i2>>>, i1
        %3 = hw.constant 0 : i1
        %2 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2x!hw.struct<x: i1, y: i2>>>, i1
        %5 = sv.reg : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i2>>>
        %4 = sv.read_inout %5 : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i2>>>
        sv.alwayscomb {
            %13 = hw.struct_create (%7, %8) : !hw.struct<x: i1, y: i2>
            %14 = hw.struct_create (%10, %11) : !hw.struct<x: i1, y: i2>
            %12 = hw.array_create %14, %13 : !hw.struct<x: i1, y: i2>
            sv.bpassign %5, %12 : !hw.array<2x!hw.struct<x: i1, y: i2>>
            sv.if %S {
                %22 = hw.struct_create (%16, %17) : !hw.struct<x: i1, y: i2>
                %23 = hw.struct_create (%19, %20) : !hw.struct<x: i1, y: i2>
                %21 = hw.array_create %23, %22 : !hw.struct<x: i1, y: i2>
                sv.bpassign %5, %21 : !hw.array<2x!hw.struct<x: i1, y: i2>>
            }
        }
        %6 = hw.array_get %0[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %7 = hw.struct_extract %6["x"] : !hw.struct<x: i1, y: i2>
        %8 = hw.struct_extract %6["y"] : !hw.struct<x: i1, y: i2>
        %9 = hw.array_get %0[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %10 = hw.struct_extract %9["x"] : !hw.struct<x: i1, y: i2>
        %11 = hw.struct_extract %9["y"] : !hw.struct<x: i1, y: i2>
        %15 = hw.array_get %2[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %16 = hw.struct_extract %15["x"] : !hw.struct<x: i1, y: i2>
        %17 = hw.struct_extract %15["y"] : !hw.struct<x: i1, y: i2>
        %18 = hw.array_get %2[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %19 = hw.struct_extract %18["x"] : !hw.struct<x: i1, y: i2>
        %20 = hw.struct_extract %18["y"] : !hw.struct<x: i1, y: i2>
        %24 = hw.array_get %4[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %25 = hw.struct_extract %24["x"] : !hw.struct<x: i1, y: i2>
        %27 = sv.wire sym @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %27, %25 : i1
        %26 = sv.read_inout %27 : !hw.inout<i1>
        %28 = hw.struct_extract %24["y"] : !hw.struct<x: i1, y: i2>
        %30 = sv.wire sym @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_False._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i2>
        sv.assign %30, %28 : i2
        %29 = sv.read_inout %30 : !hw.inout<i2>
        %31 = hw.struct_create (%26, %29) : !hw.struct<x: i1, y: i2>
        %32 = hw.array_get %4[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %33 = hw.struct_extract %32["x"] : !hw.struct<x: i1, y: i2>
        %35 = sv.wire sym @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_False._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %35, %33 : i1
        %34 = sv.read_inout %35 : !hw.inout<i1>
        %36 = hw.struct_extract %32["y"] : !hw.struct<x: i1, y: i2>
        %38 = sv.wire sym @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_False._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i2>
        sv.assign %38, %36 : i2
        %37 = sv.read_inout %38 : !hw.inout<i2>
        %39 = hw.struct_create (%34, %37) : !hw.struct<x: i1, y: i2>
        %40 = hw.array_create %39, %31 : !hw.struct<x: i1, y: i2>
        %41 = hw.array_get %2[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %42 = hw.struct_extract %41["x"] : !hw.struct<x: i1, y: i2>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %26, %42) : i1, i1, i1
        %43 = hw.struct_extract %41["y"] : !hw.struct<x: i1, y: i2>
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %29, %43) : i1, i2, i2
        %44 = hw.array_get %2[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %45 = hw.struct_extract %44["x"] : !hw.struct<x: i1, y: i2>
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %34, %45) : i1, i1, i1
        %46 = hw.struct_extract %44["y"] : !hw.struct<x: i1, y: i2>
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %37, %46) : i1, i2, i2
        %48 = hw.constant -1 : i1
        %47 = comb.xor %48, %S : i1
        %49 = hw.array_get %0[%3] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %50 = hw.struct_extract %49["x"] : !hw.struct<x: i1, y: i2>
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%47, %26, %50) : i1, i1, i1
        %51 = comb.xor %48, %S : i1
        %52 = hw.struct_extract %49["y"] : !hw.struct<x: i1, y: i2>
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %29, %52) : i1, i2, i2
        %53 = comb.xor %48, %S : i1
        %54 = hw.array_get %0[%1] : !hw.array<2x!hw.struct<x: i1, y: i2>>, i1
        %55 = hw.struct_extract %54["x"] : !hw.struct<x: i1, y: i2>
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%53, %34, %55) : i1, i1, i1
        %56 = comb.xor %48, %S : i1
        %57 = hw.struct_extract %54["y"] : !hw.struct<x: i1, y: i2>
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%56, %37, %57) : i1, i2, i2
        hw.output %40 : !hw.array<2x!hw.struct<x: i1, y: i2>>
    }
}
