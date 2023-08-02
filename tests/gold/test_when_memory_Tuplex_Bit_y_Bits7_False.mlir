module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Memory(%RADDR: i5, %CLK: i1, %WADDR: i5, %WDATA: !hw.struct<x: i1, y: i7>, %WE: i1) -> (RDATA: !hw.struct<x: i1, y: i7>) {
        %0 = hw.struct_extract %WDATA["x"] : !hw.struct<x: i1, y: i7>
        %1 = hw.struct_extract %WDATA["y"] : !hw.struct<x: i1, y: i7>
        %2 = comb.extract %1 from 0 : (i7) -> i1
        %3 = comb.extract %1 from 1 : (i7) -> i1
        %4 = comb.extract %1 from 2 : (i7) -> i1
        %5 = comb.extract %1 from 3 : (i7) -> i1
        %6 = comb.extract %1 from 4 : (i7) -> i1
        %7 = comb.extract %1 from 5 : (i7) -> i1
        %8 = comb.extract %1 from 6 : (i7) -> i1
        %9 = comb.concat %8, %7, %6, %5, %4, %3, %2, %0 : i1, i1, i1, i1, i1, i1, i1, i1
        %11 = sv.reg name "coreir_mem32x8_inst0" : !hw.inout<!hw.array<32xi8>>
        %12 = sv.array_index_inout %11[%RADDR] : !hw.inout<!hw.array<32xi8>>, i5
        %10 = sv.read_inout %12 : !hw.inout<i8>
        %13 = sv.array_index_inout %11[%WADDR] : !hw.inout<!hw.array<32xi8>>, i5
        sv.alwaysff(posedge %CLK) {
            sv.if %WE {
                sv.passign %13, %9 : i8
            }
        }
        %14 = comb.extract %10 from 0 : (i8) -> i1
        %15 = comb.extract %10 from 1 : (i8) -> i1
        %16 = comb.extract %10 from 2 : (i8) -> i1
        %17 = comb.extract %10 from 3 : (i8) -> i1
        %18 = comb.extract %10 from 4 : (i8) -> i1
        %19 = comb.extract %10 from 5 : (i8) -> i1
        %20 = comb.extract %10 from 6 : (i8) -> i1
        %21 = comb.extract %10 from 7 : (i8) -> i1
        %22 = comb.concat %21, %20, %19, %18, %17, %16, %15 : i1, i1, i1, i1, i1, i1, i1
        %23 = hw.struct_create (%14, %22) : !hw.struct<x: i1, y: i7>
        hw.output %23 : !hw.struct<x: i1, y: i7>
    }
    hw.module @test_when_memory_Tuplex_Bit_y_Bits7_False(%data0: !hw.struct<x: i1, y: i7>, %addr0: i5, %en0: i1, %data1: !hw.struct<x: i1, y: i7>, %addr1: i5, %en1: i1, %CLK: i1) -> (out: !hw.struct<x: i1, y: i7>) {
        %0 = hw.constant 1 : i1
        %3 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i5>
        sv.assign %3, %1 : i5
        %2 = sv.read_inout %3 : !hw.inout<i5>
        %6 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i5>
        sv.assign %6, %4 : i5
        %5 = sv.read_inout %6 : !hw.inout<i5>
        %8 = hw.struct_extract %7["x"] : !hw.struct<x: i1, y: i7>
        %10 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i1>
        sv.assign %10, %8 : i1
        %9 = sv.read_inout %10 : !hw.inout<i1>
        %11 = hw.struct_extract %7["y"] : !hw.struct<x: i1, y: i7>
        %13 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_7 name "_WHEN_ASSERT_7" : !hw.inout<i7>
        sv.assign %13, %11 : i7
        %12 = sv.read_inout %13 : !hw.inout<i7>
        %14 = hw.struct_create (%9, %12) : !hw.struct<x: i1, y: i7>
        %17 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %17, %15 : i1
        %16 = sv.read_inout %17 : !hw.inout<i1>
        %18 = hw.instance "Memory_inst0" @Memory(RADDR: %2: i5, CLK: %CLK: i1, WADDR: %5: i5, WDATA: %14: !hw.struct<x: i1, y: i7>, WE: %16: i1) -> (RDATA: !hw.struct<x: i1, y: i7>)
        %19 = hw.constant 127 : i7
        %20 = hw.constant 0 : i5
        %21 = hw.constant 0 : i1
        %22 = hw.constant 0 : i7
        %23 = hw.struct_create (%21, %22) : !hw.struct<x: i1, y: i7>
        %24 = hw.constant 0 : i1
        %25 = hw.constant 0 : i5
        %26 = hw.constant 0 : i7
        %28 = sv.reg : !hw.inout<i5>
        %4 = sv.read_inout %28 : !hw.inout<i5>
        %29 = sv.reg : !hw.inout<!hw.struct<x: i1, y: i7>>
        %7 = sv.read_inout %29 : !hw.inout<!hw.struct<x: i1, y: i7>>
        %30 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %30 : !hw.inout<i1>
        %31 = sv.reg : !hw.inout<i5>
        %1 = sv.read_inout %31 : !hw.inout<i5>
        %32 = sv.reg : !hw.inout<!hw.struct<x: i1, y: i7>>
        %27 = sv.read_inout %32 : !hw.inout<!hw.struct<x: i1, y: i7>>
        sv.alwayscomb {
            sv.bpassign %28, %20 : i5
            sv.bpassign %30, %24 : i1
            sv.bpassign %31, %25 : i5
            %33 = hw.struct_create (%24, %26) : !hw.struct<x: i1, y: i7>
            sv.bpassign %29, %33 : !hw.struct<x: i1, y: i7>
            sv.if %en0 {
                sv.bpassign %28, %addr0 : i5
                sv.bpassign %30, %0 : i1
                sv.bpassign %31, %addr1 : i5
                %38 = hw.struct_create (%34, %35) : !hw.struct<x: i1, y: i7>
                sv.bpassign %32, %38 : !hw.struct<x: i1, y: i7>
                %39 = hw.struct_create (%36, %37) : !hw.struct<x: i1, y: i7>
                sv.bpassign %29, %39 : !hw.struct<x: i1, y: i7>
            } else {
                sv.if %en1 {
                    sv.bpassign %28, %addr1 : i5
                    sv.bpassign %30, %0 : i1
                    sv.bpassign %31, %addr0 : i5
                    %42 = hw.struct_create (%34, %35) : !hw.struct<x: i1, y: i7>
                    sv.bpassign %32, %42 : !hw.struct<x: i1, y: i7>
                    %43 = hw.struct_create (%40, %41) : !hw.struct<x: i1, y: i7>
                    sv.bpassign %29, %43 : !hw.struct<x: i1, y: i7>
                } else {
                    %44 = hw.struct_create (%0, %19) : !hw.struct<x: i1, y: i7>
                    sv.bpassign %32, %44 : !hw.struct<x: i1, y: i7>
                }
            }
        }
        %34 = hw.struct_extract %18["x"] : !hw.struct<x: i1, y: i7>
        %35 = hw.struct_extract %18["y"] : !hw.struct<x: i1, y: i7>
        %36 = hw.struct_extract %data0["x"] : !hw.struct<x: i1, y: i7>
        %37 = hw.struct_extract %data0["y"] : !hw.struct<x: i1, y: i7>
        %40 = hw.struct_extract %data1["x"] : !hw.struct<x: i1, y: i7>
        %41 = hw.struct_extract %data1["y"] : !hw.struct<x: i1, y: i7>
        %45 = hw.struct_extract %27["x"] : !hw.struct<x: i1, y: i7>
        %47 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %47, %45 : i1
        %46 = sv.read_inout %47 : !hw.inout<i1>
        %48 = hw.struct_extract %27["y"] : !hw.struct<x: i1, y: i7>
        %50 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i7>
        sv.assign %50, %48 : i7
        %49 = sv.read_inout %50 : !hw.inout<i7>
        %51 = hw.struct_create (%46, %49) : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %5, %addr0) : i1, i5, i5
        %52 = hw.struct_create (%9, %12) : !hw.struct<x: i1, y: i7>
        %54 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<!hw.struct<x: i1, y: i7>>
        sv.assign %54, %52 : !hw.struct<x: i1, y: i7>
        %53 = sv.read_inout %54 : !hw.inout<!hw.struct<x: i1, y: i7>>
        %55 = hw.struct_extract %53["y"] : !hw.struct<x: i1, y: i7>
        %56 = hw.struct_extract %53["x"] : !hw.struct<x: i1, y: i7>
        %57 = hw.struct_extract %data0["y"] : !hw.struct<x: i1, y: i7>
        %58 = hw.struct_extract %data0["x"] : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%en0, %55, %56, %57, %58) : i1, i7, i1, i7, i1
        %59 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %16, %59) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %2, %addr1) : i1, i5, i5
        %60 = hw.struct_extract %18["x"] : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %46, %60) : i1, i1, i1
        %61 = hw.struct_extract %18["y"] : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %49, %61) : i1, i7, i7
        %63 = hw.constant -1 : i1
        %62 = comb.xor %63, %en0 : i1
        %64 = comb.and %62, %en1 : i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%64, %5, %addr1) : i1, i5, i5
        %65 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%64, %16, %65) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%64, %2, %addr0) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%64, %46, %60) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%64, %49, %61) : i1, i7, i7
        %66 = hw.struct_extract %data1["x"] : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%64, %9, %66) : i1, i1, i1
        %67 = hw.struct_extract %data1["y"] : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%64, %12, %67) : i1, i7, i7
        %68 = comb.xor %63, %en1 : i1
        %69 = comb.and %62, %68 : i1
        %70 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%69, %46, %70) : i1, i1, i1
        %71 = hw.constant 127 : i7
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%69, %49, %71) : i1, i7, i7
        %72 = comb.or %en0, %64 : i1
        %73 = comb.xor %63, %72 : i1
        %74 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%73, %5, %74) : i1, i5, i5
        %75 = comb.or %en0, %64 : i1
        %76 = comb.xor %63, %75 : i1
        %77 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%76, %16, %77) : i1, i1, i1
        %78 = comb.or %en0, %64 : i1
        %79 = comb.xor %63, %78 : i1
        %80 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%79, %2, %80) : i1, i5, i5
        %81 = comb.xor %63, %64 : i1
        %82 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_18: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%81, %9, %82) : i1, i1, i1
        %83 = comb.xor %63, %64 : i1
        %84 = hw.constant 0 : i7
        sv.verbatim "WHEN_ASSERT_19: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%83, %12, %84) : i1, i7, i7
        hw.output %51 : !hw.struct<x: i1, y: i7>
    }
}
