module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Memory(in %RADDR: i5, in %CLK: i1, in %WADDR: i5, in %WDATA: !hw.struct<x: i1, y: i7>, in %WE: i1, out RDATA: !hw.struct<x: i1, y: i7>) {
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
    hw.module @test_when_memory_Tuplex_Bit_y_Bits7_False(in %data0: !hw.struct<x: i1, y: i7>, in %addr0: i5, in %en0: i1, in %data1: !hw.struct<x: i1, y: i7>, in %addr1: i5, in %en1: i1, in %CLK: i1, out out: !hw.struct<x: i1, y: i7>) {
        %0 = hw.constant 1 : i1
        %3 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i5>
        sv.assign %3, %1 : i5
        %2 = sv.read_inout %3 : !hw.inout<i5>
        %6 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i5>
        sv.assign %6, %4 : i5
        %5 = sv.read_inout %6 : !hw.inout<i5>
        %9 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<!hw.struct<x: i1, y: i7>>
        sv.assign %9, %7 : !hw.struct<x: i1, y: i7>
        %8 = sv.read_inout %9 : !hw.inout<!hw.struct<x: i1, y: i7>>
        %12 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %12, %10 : i1
        %11 = sv.read_inout %12 : !hw.inout<i1>
        %13 = hw.instance "Memory_inst0" @Memory(RADDR: %2: i5, CLK: %CLK: i1, WADDR: %5: i5, WDATA: %8: !hw.struct<x: i1, y: i7>, WE: %11: i1) -> (RDATA: !hw.struct<x: i1, y: i7>)
        %14 = hw.constant 127 : i7
        %15 = hw.constant 0 : i5
        %16 = hw.constant 0 : i1
        %17 = hw.constant 0 : i7
        %18 = hw.struct_create (%16, %17) : !hw.struct<x: i1, y: i7>
        %19 = hw.constant 0 : i1
        %20 = hw.constant 0 : i5
        %22 = sv.reg : !hw.inout<i5>
        %4 = sv.read_inout %22 : !hw.inout<i5>
        %23 = sv.reg : !hw.inout<!hw.struct<x: i1, y: i7>>
        %7 = sv.read_inout %23 : !hw.inout<!hw.struct<x: i1, y: i7>>
        %24 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %24 : !hw.inout<i1>
        %25 = sv.reg : !hw.inout<i5>
        %1 = sv.read_inout %25 : !hw.inout<i5>
        %26 = sv.reg : !hw.inout<!hw.struct<x: i1, y: i7>>
        %21 = sv.read_inout %26 : !hw.inout<!hw.struct<x: i1, y: i7>>
        sv.alwayscomb {
            sv.bpassign %22, %15 : i5
            sv.bpassign %23, %18 : !hw.struct<x: i1, y: i7>
            sv.bpassign %24, %19 : i1
            sv.bpassign %25, %20 : i5
            sv.if %en0 {
                sv.bpassign %22, %addr0 : i5
                sv.bpassign %23, %data0 : !hw.struct<x: i1, y: i7>
                sv.bpassign %24, %0 : i1
                sv.bpassign %25, %addr1 : i5
                %29 = hw.struct_create (%27, %28) : !hw.struct<x: i1, y: i7>
                sv.bpassign %26, %29 : !hw.struct<x: i1, y: i7>
            } else {
                sv.if %en1 {
                    sv.bpassign %22, %addr1 : i5
                    sv.bpassign %23, %data1 : !hw.struct<x: i1, y: i7>
                    sv.bpassign %24, %0 : i1
                    sv.bpassign %25, %addr0 : i5
                    %30 = hw.struct_create (%27, %28) : !hw.struct<x: i1, y: i7>
                    sv.bpassign %26, %30 : !hw.struct<x: i1, y: i7>
                } else {
                    %31 = hw.struct_create (%0, %14) : !hw.struct<x: i1, y: i7>
                    sv.bpassign %26, %31 : !hw.struct<x: i1, y: i7>
                }
            }
        }
        %27 = hw.struct_extract %13["x"] : !hw.struct<x: i1, y: i7>
        %28 = hw.struct_extract %13["y"] : !hw.struct<x: i1, y: i7>
        %32 = hw.struct_extract %21["x"] : !hw.struct<x: i1, y: i7>
        %34 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i1>
        sv.assign %34, %32 : i1
        %33 = sv.read_inout %34 : !hw.inout<i1>
        %35 = hw.struct_extract %21["y"] : !hw.struct<x: i1, y: i7>
        %37 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7_False._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i7>
        sv.assign %37, %35 : i7
        %36 = sv.read_inout %37 : !hw.inout<i7>
        %38 = hw.struct_create (%33, %36) : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %5, %addr0) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %8, %data0) : i1, !hw.struct<x: i1, y: i7>, !hw.struct<x: i1, y: i7>
        %39 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %11, %39) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %2, %addr1) : i1, i5, i5
        %40 = hw.struct_extract %13["x"] : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %33, %40) : i1, i1, i1
        %41 = hw.struct_extract %13["y"] : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %36, %41) : i1, i7, i7
        %43 = hw.constant -1 : i1
        %42 = comb.xor %43, %en0 : i1
        %44 = comb.and %42, %en1 : i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%44, %5, %addr1) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%44, %8, %data1) : i1, !hw.struct<x: i1, y: i7>, !hw.struct<x: i1, y: i7>
        %45 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%44, %11, %45) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%44, %2, %addr0) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%44, %33, %40) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%44, %36, %41) : i1, i7, i7
        %46 = comb.xor %43, %en1 : i1
        %47 = comb.and %42, %46 : i1
        %48 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%47, %33, %48) : i1, i1, i1
        %49 = hw.constant 127 : i7
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%47, %36, %49) : i1, i7, i7
        %50 = comb.or %en0, %44 : i1
        %51 = comb.xor %43, %50 : i1
        %52 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %5, %52) : i1, i5, i5
        %53 = comb.or %en0, %44 : i1
        %54 = comb.xor %43, %53 : i1
        %55 = hw.constant 0 : i1
        %56 = hw.constant 0 : i7
        %57 = hw.struct_create (%55, %56) : !hw.struct<x: i1, y: i7>
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%54, %8, %57) : i1, !hw.struct<x: i1, y: i7>, !hw.struct<x: i1, y: i7>
        %58 = comb.or %en0, %44 : i1
        %59 = comb.xor %43, %58 : i1
        %60 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%59, %11, %60) : i1, i1, i1
        %61 = comb.or %en0, %44 : i1
        %62 = comb.xor %43, %61 : i1
        %63 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%62, %2, %63) : i1, i5, i5
        hw.output %38 : !hw.struct<x: i1, y: i7>
    }
}
