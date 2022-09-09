hw.module @Memory(%RADDR: i5, %CLK: i1, %WADDR: i5, %WDATA: i8, %WE: i1) -> (RDATA: i8) {
    %1 = sv.reg {name = "coreir_mem32x8_inst0"} : !hw.inout<!hw.array<32xi8>>
    %2 = sv.array_index_inout %1[%RADDR] : !hw.inout<!hw.array<32xi8>>, i5
    %0 = sv.read_inout %2 : !hw.inout<i8>
    %3 = sv.array_index_inout %1[%WADDR] : !hw.inout<!hw.array<32xi8>>, i5
    sv.alwaysff(posedge %CLK) {
        sv.if %WE {
            sv.passign %3, %WDATA : i8
        }
    }
    hw.output %0 : i8
}
hw.module @test_when_memory_Bits8(%data0: i8, %addr0: i5, %en0: i1, %data1: i8, %addr1: i5, %en1: i1, %CLK: i1) -> (out: i8) {
    %0 = hw.constant 1 : i1
    %1 = comb.extract %addr0 from 0 : (i5) -> i1
    %2 = comb.extract %addr1 from 0 : (i5) -> i1
    %3 = comb.extract %addr0 from 1 : (i5) -> i1
    %4 = comb.extract %addr1 from 1 : (i5) -> i1
    %5 = comb.extract %addr0 from 2 : (i5) -> i1
    %6 = comb.extract %addr1 from 2 : (i5) -> i1
    %7 = comb.extract %addr0 from 3 : (i5) -> i1
    %8 = comb.extract %addr1 from 3 : (i5) -> i1
    %9 = comb.extract %addr0 from 4 : (i5) -> i1
    %10 = comb.extract %addr1 from 4 : (i5) -> i1
    %11 = comb.extract %data0 from 0 : (i8) -> i1
    %12 = comb.extract %data1 from 0 : (i8) -> i1
    %13 = comb.extract %data0 from 1 : (i8) -> i1
    %14 = comb.extract %data1 from 1 : (i8) -> i1
    %15 = comb.extract %data0 from 2 : (i8) -> i1
    %16 = comb.extract %data1 from 2 : (i8) -> i1
    %17 = comb.extract %data0 from 3 : (i8) -> i1
    %18 = comb.extract %data1 from 3 : (i8) -> i1
    %19 = comb.extract %data0 from 4 : (i8) -> i1
    %20 = comb.extract %data1 from 4 : (i8) -> i1
    %21 = comb.extract %data0 from 5 : (i8) -> i1
    %22 = comb.extract %data1 from 5 : (i8) -> i1
    %23 = comb.extract %data0 from 6 : (i8) -> i1
    %24 = comb.extract %data1 from 6 : (i8) -> i1
    %25 = comb.extract %data0 from 7 : (i8) -> i1
    %26 = comb.extract %data1 from 7 : (i8) -> i1
    %32 = comb.concat %31, %30, %29, %28, %27 : i1, i1, i1, i1, i1
    %38 = comb.concat %37, %36, %35, %34, %33 : i1, i1, i1, i1, i1
    %47 = comb.concat %46, %45, %44, %43, %42, %41, %40, %39 : i1, i1, i1, i1, i1, i1, i1, i1
    %49 = hw.instance "Memory_inst0" @Memory(RADDR: %32: i5, CLK: %CLK: i1, WADDR: %38: i5, WDATA: %47: i8, WE: %48: i1) -> (RDATA: i8)
    %50 = comb.extract %49 from 0 : (i8) -> i1
    %51 = comb.extract %49 from 1 : (i8) -> i1
    %52 = comb.extract %49 from 2 : (i8) -> i1
    %53 = comb.extract %49 from 3 : (i8) -> i1
    %54 = comb.extract %49 from 4 : (i8) -> i1
    %55 = comb.extract %49 from 5 : (i8) -> i1
    %56 = comb.extract %49 from 6 : (i8) -> i1
    %57 = comb.extract %49 from 7 : (i8) -> i1
    %58 = hw.constant 0 : i1
    %67 = sv.reg : !hw.inout<i1>
    %48 = sv.read_inout %67 : !hw.inout<i1>
    %68 = sv.reg : !hw.inout<i1>
    %33 = sv.read_inout %68 : !hw.inout<i1>
    %69 = sv.reg : !hw.inout<i1>
    %34 = sv.read_inout %69 : !hw.inout<i1>
    %70 = sv.reg : !hw.inout<i1>
    %35 = sv.read_inout %70 : !hw.inout<i1>
    %71 = sv.reg : !hw.inout<i1>
    %36 = sv.read_inout %71 : !hw.inout<i1>
    %72 = sv.reg : !hw.inout<i1>
    %37 = sv.read_inout %72 : !hw.inout<i1>
    %73 = sv.reg : !hw.inout<i1>
    %39 = sv.read_inout %73 : !hw.inout<i1>
    %74 = sv.reg : !hw.inout<i1>
    %40 = sv.read_inout %74 : !hw.inout<i1>
    %75 = sv.reg : !hw.inout<i1>
    %41 = sv.read_inout %75 : !hw.inout<i1>
    %76 = sv.reg : !hw.inout<i1>
    %42 = sv.read_inout %76 : !hw.inout<i1>
    %77 = sv.reg : !hw.inout<i1>
    %43 = sv.read_inout %77 : !hw.inout<i1>
    %78 = sv.reg : !hw.inout<i1>
    %44 = sv.read_inout %78 : !hw.inout<i1>
    %79 = sv.reg : !hw.inout<i1>
    %45 = sv.read_inout %79 : !hw.inout<i1>
    %80 = sv.reg : !hw.inout<i1>
    %46 = sv.read_inout %80 : !hw.inout<i1>
    %81 = sv.reg : !hw.inout<i1>
    %27 = sv.read_inout %81 : !hw.inout<i1>
    %82 = sv.reg : !hw.inout<i1>
    %28 = sv.read_inout %82 : !hw.inout<i1>
    %83 = sv.reg : !hw.inout<i1>
    %29 = sv.read_inout %83 : !hw.inout<i1>
    %84 = sv.reg : !hw.inout<i1>
    %30 = sv.read_inout %84 : !hw.inout<i1>
    %85 = sv.reg : !hw.inout<i1>
    %31 = sv.read_inout %85 : !hw.inout<i1>
    %86 = sv.reg : !hw.inout<i1>
    %59 = sv.read_inout %86 : !hw.inout<i1>
    %87 = sv.reg : !hw.inout<i1>
    %60 = sv.read_inout %87 : !hw.inout<i1>
    %88 = sv.reg : !hw.inout<i1>
    %61 = sv.read_inout %88 : !hw.inout<i1>
    %89 = sv.reg : !hw.inout<i1>
    %62 = sv.read_inout %89 : !hw.inout<i1>
    %90 = sv.reg : !hw.inout<i1>
    %63 = sv.read_inout %90 : !hw.inout<i1>
    %91 = sv.reg : !hw.inout<i1>
    %64 = sv.read_inout %91 : !hw.inout<i1>
    %92 = sv.reg : !hw.inout<i1>
    %65 = sv.read_inout %92 : !hw.inout<i1>
    %93 = sv.reg : !hw.inout<i1>
    %66 = sv.read_inout %93 : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %68, %1 : i1
        sv.bpassign %69, %3 : i1
        sv.bpassign %70, %5 : i1
        sv.bpassign %71, %7 : i1
        sv.bpassign %72, %9 : i1
        sv.bpassign %73, %11 : i1
        sv.bpassign %74, %13 : i1
        sv.bpassign %75, %15 : i1
        sv.bpassign %76, %17 : i1
        sv.bpassign %77, %19 : i1
        sv.bpassign %78, %21 : i1
        sv.bpassign %79, %23 : i1
        sv.bpassign %80, %25 : i1
        sv.bpassign %81, %2 : i1
        sv.bpassign %82, %4 : i1
        sv.bpassign %83, %6 : i1
        sv.bpassign %84, %8 : i1
        sv.bpassign %85, %10 : i1
        sv.bpassign %86, %50 : i1
        sv.bpassign %87, %51 : i1
        sv.bpassign %88, %52 : i1
        sv.bpassign %89, %53 : i1
        sv.bpassign %90, %54 : i1
        sv.bpassign %91, %55 : i1
        sv.bpassign %92, %56 : i1
        sv.bpassign %93, %57 : i1
        sv.bpassign %67, %58 : i1
        sv.if %en0 {
            sv.bpassign %67, %0 : i1
        } else {
            sv.if %en1 {
                sv.bpassign %68, %2 : i1
                sv.bpassign %69, %4 : i1
                sv.bpassign %70, %6 : i1
                sv.bpassign %71, %8 : i1
                sv.bpassign %72, %10 : i1
                sv.bpassign %73, %12 : i1
                sv.bpassign %74, %14 : i1
                sv.bpassign %75, %16 : i1
                sv.bpassign %76, %18 : i1
                sv.bpassign %77, %20 : i1
                sv.bpassign %78, %22 : i1
                sv.bpassign %79, %24 : i1
                sv.bpassign %80, %26 : i1
                sv.bpassign %67, %0 : i1
                sv.bpassign %81, %1 : i1
                sv.bpassign %82, %3 : i1
                sv.bpassign %83, %5 : i1
                sv.bpassign %84, %7 : i1
                sv.bpassign %85, %9 : i1
                sv.bpassign %86, %50 : i1
                sv.bpassign %87, %51 : i1
                sv.bpassign %88, %52 : i1
                sv.bpassign %89, %53 : i1
                sv.bpassign %90, %54 : i1
                sv.bpassign %91, %55 : i1
                sv.bpassign %92, %56 : i1
                sv.bpassign %93, %57 : i1
            } else {
                sv.bpassign %86, %0 : i1
                sv.bpassign %87, %0 : i1
                sv.bpassign %88, %0 : i1
                sv.bpassign %89, %0 : i1
                sv.bpassign %90, %0 : i1
                sv.bpassign %91, %0 : i1
                sv.bpassign %92, %0 : i1
                sv.bpassign %93, %0 : i1
            }
        }
    }
    %94 = comb.concat %66, %65, %64, %63, %62, %61, %60, %59 : i1, i1, i1, i1, i1, i1, i1, i1
    hw.output %94 : i8
}
