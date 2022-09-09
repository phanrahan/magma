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
    %0 = comb.extract %addr0 from 0 : (i5) -> i1
    %1 = comb.extract %addr0 from 1 : (i5) -> i1
    %2 = comb.extract %addr0 from 2 : (i5) -> i1
    %3 = comb.extract %addr0 from 3 : (i5) -> i1
    %4 = comb.extract %addr0 from 4 : (i5) -> i1
    %5 = comb.extract %data0 from 0 : (i8) -> i1
    %6 = comb.extract %data0 from 1 : (i8) -> i1
    %7 = comb.extract %data0 from 2 : (i8) -> i1
    %8 = comb.extract %data0 from 3 : (i8) -> i1
    %9 = comb.extract %data0 from 4 : (i8) -> i1
    %10 = comb.extract %data0 from 5 : (i8) -> i1
    %11 = comb.extract %data0 from 6 : (i8) -> i1
    %12 = comb.extract %data0 from 7 : (i8) -> i1
    %13 = hw.constant 1 : i1
    %14 = comb.extract %addr1 from 0 : (i5) -> i1
    %15 = comb.extract %addr1 from 1 : (i5) -> i1
    %16 = comb.extract %addr1 from 2 : (i5) -> i1
    %17 = comb.extract %addr1 from 3 : (i5) -> i1
    %18 = comb.extract %addr1 from 4 : (i5) -> i1
    %24 = comb.concat %23, %22, %21, %20, %19 : i1, i1, i1, i1, i1
    %30 = comb.concat %29, %28, %27, %26, %25 : i1, i1, i1, i1, i1
    %39 = comb.concat %38, %37, %36, %35, %34, %33, %32, %31 : i1, i1, i1, i1, i1, i1, i1, i1
    %41 = hw.instance "Memory_inst0" @Memory(RADDR: %24: i5, CLK: %CLK: i1, WADDR: %30: i5, WDATA: %39: i8, WE: %40: i1) -> (RDATA: i8)
    %42 = comb.extract %41 from 0 : (i8) -> i1
    %43 = comb.extract %41 from 1 : (i8) -> i1
    %44 = comb.extract %41 from 2 : (i8) -> i1
    %45 = comb.extract %41 from 3 : (i8) -> i1
    %46 = comb.extract %41 from 4 : (i8) -> i1
    %47 = comb.extract %41 from 5 : (i8) -> i1
    %48 = comb.extract %41 from 6 : (i8) -> i1
    %49 = comb.extract %41 from 7 : (i8) -> i1
    %50 = comb.extract %data1 from 0 : (i8) -> i1
    %51 = comb.extract %data1 from 1 : (i8) -> i1
    %52 = comb.extract %data1 from 2 : (i8) -> i1
    %53 = comb.extract %data1 from 3 : (i8) -> i1
    %54 = comb.extract %data1 from 4 : (i8) -> i1
    %55 = comb.extract %data1 from 5 : (i8) -> i1
    %56 = comb.extract %data1 from 6 : (i8) -> i1
    %57 = comb.extract %data1 from 7 : (i8) -> i1
    %58 = hw.constant 0 : i1
    %67 = sv.reg : !hw.inout<i1>
    %25 = sv.read_inout %67 : !hw.inout<i1>
    %68 = sv.reg : !hw.inout<i1>
    %26 = sv.read_inout %68 : !hw.inout<i1>
    %69 = sv.reg : !hw.inout<i1>
    %27 = sv.read_inout %69 : !hw.inout<i1>
    %70 = sv.reg : !hw.inout<i1>
    %28 = sv.read_inout %70 : !hw.inout<i1>
    %71 = sv.reg : !hw.inout<i1>
    %29 = sv.read_inout %71 : !hw.inout<i1>
    %72 = sv.reg : !hw.inout<i1>
    %31 = sv.read_inout %72 : !hw.inout<i1>
    %73 = sv.reg : !hw.inout<i1>
    %32 = sv.read_inout %73 : !hw.inout<i1>
    %74 = sv.reg : !hw.inout<i1>
    %33 = sv.read_inout %74 : !hw.inout<i1>
    %75 = sv.reg : !hw.inout<i1>
    %34 = sv.read_inout %75 : !hw.inout<i1>
    %76 = sv.reg : !hw.inout<i1>
    %35 = sv.read_inout %76 : !hw.inout<i1>
    %77 = sv.reg : !hw.inout<i1>
    %36 = sv.read_inout %77 : !hw.inout<i1>
    %78 = sv.reg : !hw.inout<i1>
    %37 = sv.read_inout %78 : !hw.inout<i1>
    %79 = sv.reg : !hw.inout<i1>
    %38 = sv.read_inout %79 : !hw.inout<i1>
    %80 = sv.reg : !hw.inout<i1>
    %40 = sv.read_inout %80 : !hw.inout<i1>
    %81 = sv.reg : !hw.inout<i1>
    %19 = sv.read_inout %81 : !hw.inout<i1>
    %82 = sv.reg : !hw.inout<i1>
    %20 = sv.read_inout %82 : !hw.inout<i1>
    %83 = sv.reg : !hw.inout<i1>
    %21 = sv.read_inout %83 : !hw.inout<i1>
    %84 = sv.reg : !hw.inout<i1>
    %22 = sv.read_inout %84 : !hw.inout<i1>
    %85 = sv.reg : !hw.inout<i1>
    %23 = sv.read_inout %85 : !hw.inout<i1>
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
        sv.bpassign %67, %58 : i1
        sv.bpassign %68, %58 : i1
        sv.bpassign %69, %58 : i1
        sv.bpassign %70, %58 : i1
        sv.bpassign %71, %58 : i1
        sv.bpassign %72, %58 : i1
        sv.bpassign %73, %58 : i1
        sv.bpassign %74, %58 : i1
        sv.bpassign %75, %58 : i1
        sv.bpassign %76, %58 : i1
        sv.bpassign %77, %58 : i1
        sv.bpassign %78, %58 : i1
        sv.bpassign %79, %58 : i1
        sv.bpassign %80, %58 : i1
        sv.bpassign %81, %58 : i1
        sv.bpassign %82, %58 : i1
        sv.bpassign %83, %58 : i1
        sv.bpassign %84, %58 : i1
        sv.bpassign %85, %58 : i1
        sv.if %en0 {
            sv.bpassign %67, %0 : i1
            sv.bpassign %68, %1 : i1
            sv.bpassign %69, %2 : i1
            sv.bpassign %70, %3 : i1
            sv.bpassign %71, %4 : i1
            sv.bpassign %72, %5 : i1
            sv.bpassign %73, %6 : i1
            sv.bpassign %74, %7 : i1
            sv.bpassign %75, %8 : i1
            sv.bpassign %76, %9 : i1
            sv.bpassign %77, %10 : i1
            sv.bpassign %78, %11 : i1
            sv.bpassign %79, %12 : i1
            sv.bpassign %80, %13 : i1
            sv.bpassign %81, %14 : i1
            sv.bpassign %82, %15 : i1
            sv.bpassign %83, %16 : i1
            sv.bpassign %84, %17 : i1
            sv.bpassign %85, %18 : i1
            sv.bpassign %86, %42 : i1
            sv.bpassign %87, %43 : i1
            sv.bpassign %88, %44 : i1
            sv.bpassign %89, %45 : i1
            sv.bpassign %90, %46 : i1
            sv.bpassign %91, %47 : i1
            sv.bpassign %92, %48 : i1
            sv.bpassign %93, %49 : i1
        } else {
            sv.if %en1 {
                sv.bpassign %67, %14 : i1
                sv.bpassign %68, %15 : i1
                sv.bpassign %69, %16 : i1
                sv.bpassign %70, %17 : i1
                sv.bpassign %71, %18 : i1
                sv.bpassign %72, %50 : i1
                sv.bpassign %73, %51 : i1
                sv.bpassign %74, %52 : i1
                sv.bpassign %75, %53 : i1
                sv.bpassign %76, %54 : i1
                sv.bpassign %77, %55 : i1
                sv.bpassign %78, %56 : i1
                sv.bpassign %79, %57 : i1
                sv.bpassign %80, %13 : i1
                sv.bpassign %81, %0 : i1
                sv.bpassign %82, %1 : i1
                sv.bpassign %83, %2 : i1
                sv.bpassign %84, %3 : i1
                sv.bpassign %85, %4 : i1
                sv.bpassign %86, %42 : i1
                sv.bpassign %87, %43 : i1
                sv.bpassign %88, %44 : i1
                sv.bpassign %89, %45 : i1
                sv.bpassign %90, %46 : i1
                sv.bpassign %91, %47 : i1
                sv.bpassign %92, %48 : i1
                sv.bpassign %93, %49 : i1
            } else {
                sv.bpassign %86, %13 : i1
                sv.bpassign %87, %13 : i1
                sv.bpassign %88, %13 : i1
                sv.bpassign %89, %13 : i1
                sv.bpassign %90, %13 : i1
                sv.bpassign %91, %13 : i1
                sv.bpassign %92, %13 : i1
                sv.bpassign %93, %13 : i1
            }
        }
    }
    %94 = comb.concat %66, %65, %64, %63, %62, %61, %60, %59 : i1, i1, i1, i1, i1, i1, i1, i1
    hw.output %94 : i8
}
