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
        %5 = hw.instance "Memory_inst0" @Memory(RADDR: %1: i5, CLK: %CLK: i1, WADDR: %2: i5, WDATA: %3: !hw.struct<x: i1, y: i7>, WE: %4: i1) -> (RDATA: !hw.struct<x: i1, y: i7>)
        %6 = hw.constant 127 : i7
        %7 = hw.constant 0 : i5
        %8 = hw.constant 0 : i1
        %9 = hw.constant 0 : i7
        %10 = hw.struct_create (%8, %9) : !hw.struct<x: i1, y: i7>
        %11 = hw.constant 0 : i1
        %12 = hw.constant 0 : i5
        %14 = sv.reg : !hw.inout<i5>
        %2 = sv.read_inout %14 : !hw.inout<i5>
        %15 = sv.reg : !hw.inout<!hw.struct<x: i1, y: i7>>
        %3 = sv.read_inout %15 : !hw.inout<!hw.struct<x: i1, y: i7>>
        %16 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg : !hw.inout<i5>
        %1 = sv.read_inout %17 : !hw.inout<i5>
        %18 = sv.reg : !hw.inout<!hw.struct<x: i1, y: i7>>
        %13 = sv.read_inout %18 : !hw.inout<!hw.struct<x: i1, y: i7>>
        sv.alwayscomb {
            sv.bpassign %14, %7 : i5
            sv.bpassign %15, %10 : !hw.struct<x: i1, y: i7>
            sv.bpassign %16, %11 : i1
            sv.bpassign %17, %12 : i5
            sv.if %en0 {
                sv.bpassign %14, %addr0 : i5
                sv.bpassign %15, %data0 : !hw.struct<x: i1, y: i7>
                sv.bpassign %16, %0 : i1
                sv.bpassign %17, %addr1 : i5
                %21 = hw.struct_create (%19, %20) : !hw.struct<x: i1, y: i7>
                sv.bpassign %18, %21 : !hw.struct<x: i1, y: i7>
            } else {
                sv.if %en1 {
                    sv.bpassign %14, %addr1 : i5
                    sv.bpassign %15, %data1 : !hw.struct<x: i1, y: i7>
                    sv.bpassign %16, %0 : i1
                    sv.bpassign %17, %addr0 : i5
                    %22 = hw.struct_create (%19, %20) : !hw.struct<x: i1, y: i7>
                    sv.bpassign %18, %22 : !hw.struct<x: i1, y: i7>
                } else {
                    %23 = hw.struct_create (%0, %6) : !hw.struct<x: i1, y: i7>
                    sv.bpassign %18, %23 : !hw.struct<x: i1, y: i7>
                }
            }
        }
        %19 = hw.struct_extract %5["x"] : !hw.struct<x: i1, y: i7>
        %20 = hw.struct_extract %5["y"] : !hw.struct<x: i1, y: i7>
        hw.output %13 : !hw.struct<x: i1, y: i7>
    }
}
