hw.module @Memory(%RADDR: i5, %CLK: i1, %WADDR: i5, %WDATA: !hw.struct<_0: i1, _1: i7>, %WE: i1) -> (RDATA: !hw.struct<_0: i1, _1: i7>) {
    %0 = hw.struct_extract %WDATA["_0"] : !hw.struct<_0: i1, _1: i7>
    %1 = hw.struct_extract %WDATA["_1"] : !hw.struct<_0: i1, _1: i7>
    %2 = comb.extract %1 from 0 : (i7) -> i1
    %3 = comb.extract %1 from 1 : (i7) -> i1
    %4 = comb.extract %1 from 2 : (i7) -> i1
    %5 = comb.extract %1 from 3 : (i7) -> i1
    %6 = comb.extract %1 from 4 : (i7) -> i1
    %7 = comb.extract %1 from 5 : (i7) -> i1
    %8 = comb.extract %1 from 6 : (i7) -> i1
    %9 = comb.concat %8, %7, %6, %5, %4, %3, %2, %0 : i1, i1, i1, i1, i1, i1, i1, i1
    %11 = sv.reg {name = "coreir_mem32x8_inst0"} : !hw.inout<!hw.array<32xi8>>
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
    %23 = hw.struct_create (%14, %22) : !hw.struct<_0: i1, _1: i7>
    hw.output %23 : !hw.struct<_0: i1, _1: i7>
}
hw.module @test_when_memory(%data0: !hw.struct<_0: i1, _1: i7>, %addr0: i5, %en0: i1, %data1: !hw.struct<_0: i1, _1: i7>, %addr1: i5, %en1: i1, %CLK: i1) -> (out: !hw.struct<_0: i1, _1: i7>) {
    %0 = hw.struct_extract %data0["_0"] : !hw.struct<_0: i1, _1: i7>
    %1 = hw.struct_extract %data0["_1"] : !hw.struct<_0: i1, _1: i7>
    %2 = hw.constant 1 : i1
    %5 = hw.struct_create (%3, %4) : !hw.struct<_0: i1, _1: i7>
    %9 = hw.instance "Memory_inst0" @Memory(RADDR: %6: i5, CLK: %CLK: i1, WADDR: %7: i5, WDATA: %5: !hw.struct<_0: i1, _1: i7>, WE: %8: i1) -> (RDATA: !hw.struct<_0: i1, _1: i7>)
    %10 = hw.struct_extract %9["_0"] : !hw.struct<_0: i1, _1: i7>
    %11 = hw.struct_extract %9["_1"] : !hw.struct<_0: i1, _1: i7>
    %12 = hw.struct_extract %data1["_0"] : !hw.struct<_0: i1, _1: i7>
    %13 = hw.struct_extract %data1["_1"] : !hw.struct<_0: i1, _1: i7>
    %14 = hw.constant 1 : i1
    %15 = hw.constant 127 : i7
    %18 = sv.reg {name = "WADDR_reg"} : !hw.inout<i5>
    %19 = sv.reg {name = "Memory_inst0.WDATA[0]_reg"} : !hw.inout<i1>
    %20 = sv.reg {name = "Memory_inst0.WDATA[1]_reg"} : !hw.inout<i7>
    %21 = sv.reg {name = "WE_reg"} : !hw.inout<i1>
    %22 = sv.reg {name = "RADDR_reg"} : !hw.inout<i5>
    %23 = sv.reg {name = "test_when_memory.out[0]_reg"} : !hw.inout<i1>
    %24 = sv.reg {name = "test_when_memory.out[1]_reg"} : !hw.inout<i7>
    sv.alwayscomb {
        %25 = hw.constant 0 : i5
        sv.bpassign %18, %25 : i5
        %26 = hw.constant 0 : i1
        sv.bpassign %21, %26 : i1
        sv.bpassign %22, %25 : i5
        sv.if %en0 {
            sv.bpassign %18, %addr0 : i5
            sv.bpassign %19, %0 : i1
            sv.bpassign %20, %1 : i7
            sv.bpassign %21, %14 : i1
            sv.bpassign %22, %addr1 : i5
            sv.bpassign %23, %10 : i1
            sv.bpassign %24, %11 : i7
        } else {
            sv.if %en1 {
                sv.bpassign %18, %addr1 : i5
                sv.bpassign %19, %12 : i1
                sv.bpassign %20, %13 : i7
                sv.bpassign %21, %14 : i1
                sv.bpassign %22, %addr0 : i5
                sv.bpassign %23, %10 : i1
                sv.bpassign %24, %11 : i7
            } else {
                sv.bpassign %23, %14 : i1
                sv.bpassign %24, %15 : i7
            }
        }
    }
    %7 = sv.read_inout %18 : !hw.inout<i5>
    %3 = sv.read_inout %19 : !hw.inout<i1>
    %4 = sv.read_inout %20 : !hw.inout<i7>
    %8 = sv.read_inout %21 : !hw.inout<i1>
    %6 = sv.read_inout %22 : !hw.inout<i5>
    %16 = sv.read_inout %23 : !hw.inout<i1>
    %17 = sv.read_inout %24 : !hw.inout<i7>
    %27 = hw.struct_create (%16, %17) : !hw.struct<_0: i1, _1: i7>
    hw.output %27 : !hw.struct<_0: i1, _1: i7>
}
