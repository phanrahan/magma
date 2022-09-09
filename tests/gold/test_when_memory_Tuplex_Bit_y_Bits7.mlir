hw.module @Memory(%RADDR: i5, %CLK: i1, %WADDR: i5, %WDATA_x: i1, %WDATA_y: i7, %WE: i1) -> (RDATA_x: i1, RDATA_y: i7) {
    %0 = comb.extract %WDATA_y from 0 : (i7) -> i1
    %1 = comb.extract %WDATA_y from 1 : (i7) -> i1
    %2 = comb.extract %WDATA_y from 2 : (i7) -> i1
    %3 = comb.extract %WDATA_y from 3 : (i7) -> i1
    %4 = comb.extract %WDATA_y from 4 : (i7) -> i1
    %5 = comb.extract %WDATA_y from 5 : (i7) -> i1
    %6 = comb.extract %WDATA_y from 6 : (i7) -> i1
    %7 = comb.concat %6, %5, %4, %3, %2, %1, %0, %WDATA_x : i1, i1, i1, i1, i1, i1, i1, i1
    %9 = sv.reg {name = "coreir_mem32x8_inst0"} : !hw.inout<!hw.array<32xi8>>
    %10 = sv.array_index_inout %9[%RADDR] : !hw.inout<!hw.array<32xi8>>, i5
    %8 = sv.read_inout %10 : !hw.inout<i8>
    %11 = sv.array_index_inout %9[%WADDR] : !hw.inout<!hw.array<32xi8>>, i5
    sv.alwaysff(posedge %CLK) {
        sv.if %WE {
            sv.passign %11, %7 : i8
        }
    }
    %12 = comb.extract %8 from 0 : (i8) -> i1
    %13 = comb.extract %8 from 1 : (i8) -> i1
    %14 = comb.extract %8 from 2 : (i8) -> i1
    %15 = comb.extract %8 from 3 : (i8) -> i1
    %16 = comb.extract %8 from 4 : (i8) -> i1
    %17 = comb.extract %8 from 5 : (i8) -> i1
    %18 = comb.extract %8 from 6 : (i8) -> i1
    %19 = comb.extract %8 from 7 : (i8) -> i1
    %20 = comb.concat %19, %18, %17, %16, %15, %14, %13 : i1, i1, i1, i1, i1, i1, i1
    hw.output %12, %20 : i1, i7
}
hw.module @test_when_memory_Tuplex_Bit_y_Bits7(%data0_x: i1, %data0_y: i7, %addr0: i5, %en0: i1, %data1_x: i1, %data1_y: i7, %addr1: i5, %en1: i1, %CLK: i1) -> (out_x: i1, out_y: i7) {
    %0 = hw.constant 1 : i1
    %6 = comb.concat %5, %4, %3, %2, %1 : i1, i1, i1, i1, i1
    %12 = comb.concat %11, %10, %9, %8, %7 : i1, i1, i1, i1, i1
    %20 = comb.concat %19, %18, %17, %16, %15, %14, %13 : i1, i1, i1, i1, i1, i1, i1
    %23, %24 = hw.instance "Memory_inst0" @Memory(RADDR: %6: i5, CLK: %CLK: i1, WADDR: %12: i5, WDATA_x: %21: i1, WDATA_y: %20: i7, WE: %22: i1) -> (RDATA_x: i1, RDATA_y: i7)
    %25 = comb.extract %addr0 from 0 : (i5) -> i1
    %26 = comb.extract %addr1 from 0 : (i5) -> i1
    %27 = comb.extract %addr0 from 1 : (i5) -> i1
    %28 = comb.extract %addr1 from 1 : (i5) -> i1
    %29 = comb.extract %addr0 from 2 : (i5) -> i1
    %30 = comb.extract %addr1 from 2 : (i5) -> i1
    %31 = comb.extract %addr0 from 3 : (i5) -> i1
    %32 = comb.extract %addr1 from 3 : (i5) -> i1
    %33 = comb.extract %addr0 from 4 : (i5) -> i1
    %34 = comb.extract %addr1 from 4 : (i5) -> i1
    %35 = comb.extract %data0_y from 0 : (i7) -> i1
    %36 = comb.extract %data1_y from 0 : (i7) -> i1
    %37 = comb.extract %data0_y from 1 : (i7) -> i1
    %38 = comb.extract %data1_y from 1 : (i7) -> i1
    %39 = comb.extract %data0_y from 2 : (i7) -> i1
    %40 = comb.extract %data1_y from 2 : (i7) -> i1
    %41 = comb.extract %data0_y from 3 : (i7) -> i1
    %42 = comb.extract %data1_y from 3 : (i7) -> i1
    %43 = comb.extract %data0_y from 4 : (i7) -> i1
    %44 = comb.extract %data1_y from 4 : (i7) -> i1
    %45 = comb.extract %data0_y from 5 : (i7) -> i1
    %46 = comb.extract %data1_y from 5 : (i7) -> i1
    %47 = comb.extract %data0_y from 6 : (i7) -> i1
    %48 = comb.extract %data1_y from 6 : (i7) -> i1
    %49 = comb.extract %24 from 0 : (i7) -> i1
    %50 = comb.extract %24 from 1 : (i7) -> i1
    %51 = comb.extract %24 from 2 : (i7) -> i1
    %52 = comb.extract %24 from 3 : (i7) -> i1
    %53 = comb.extract %24 from 4 : (i7) -> i1
    %54 = comb.extract %24 from 5 : (i7) -> i1
    %55 = comb.extract %24 from 6 : (i7) -> i1
    %56 = hw.constant 0 : i1
    %65 = sv.reg : !hw.inout<i1>
    %21 = sv.read_inout %65 : !hw.inout<i1>
    %66 = sv.reg : !hw.inout<i1>
    %22 = sv.read_inout %66 : !hw.inout<i1>
    %67 = sv.reg : !hw.inout<i1>
    %57 = sv.read_inout %67 : !hw.inout<i1>
    %68 = sv.reg : !hw.inout<i1>
    %7 = sv.read_inout %68 : !hw.inout<i1>
    %69 = sv.reg : !hw.inout<i1>
    %8 = sv.read_inout %69 : !hw.inout<i1>
    %70 = sv.reg : !hw.inout<i1>
    %9 = sv.read_inout %70 : !hw.inout<i1>
    %71 = sv.reg : !hw.inout<i1>
    %10 = sv.read_inout %71 : !hw.inout<i1>
    %72 = sv.reg : !hw.inout<i1>
    %11 = sv.read_inout %72 : !hw.inout<i1>
    %73 = sv.reg : !hw.inout<i1>
    %13 = sv.read_inout %73 : !hw.inout<i1>
    %74 = sv.reg : !hw.inout<i1>
    %14 = sv.read_inout %74 : !hw.inout<i1>
    %75 = sv.reg : !hw.inout<i1>
    %15 = sv.read_inout %75 : !hw.inout<i1>
    %76 = sv.reg : !hw.inout<i1>
    %16 = sv.read_inout %76 : !hw.inout<i1>
    %77 = sv.reg : !hw.inout<i1>
    %17 = sv.read_inout %77 : !hw.inout<i1>
    %78 = sv.reg : !hw.inout<i1>
    %18 = sv.read_inout %78 : !hw.inout<i1>
    %79 = sv.reg : !hw.inout<i1>
    %19 = sv.read_inout %79 : !hw.inout<i1>
    %80 = sv.reg : !hw.inout<i1>
    %1 = sv.read_inout %80 : !hw.inout<i1>
    %81 = sv.reg : !hw.inout<i1>
    %2 = sv.read_inout %81 : !hw.inout<i1>
    %82 = sv.reg : !hw.inout<i1>
    %3 = sv.read_inout %82 : !hw.inout<i1>
    %83 = sv.reg : !hw.inout<i1>
    %4 = sv.read_inout %83 : !hw.inout<i1>
    %84 = sv.reg : !hw.inout<i1>
    %5 = sv.read_inout %84 : !hw.inout<i1>
    %85 = sv.reg : !hw.inout<i1>
    %58 = sv.read_inout %85 : !hw.inout<i1>
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
    sv.alwayscomb {
        sv.bpassign %68, %25 : i1
        sv.bpassign %69, %27 : i1
        sv.bpassign %70, %29 : i1
        sv.bpassign %71, %31 : i1
        sv.bpassign %72, %33 : i1
        sv.bpassign %73, %35 : i1
        sv.bpassign %74, %37 : i1
        sv.bpassign %75, %39 : i1
        sv.bpassign %76, %41 : i1
        sv.bpassign %77, %43 : i1
        sv.bpassign %78, %45 : i1
        sv.bpassign %79, %47 : i1
        sv.bpassign %80, %26 : i1
        sv.bpassign %81, %28 : i1
        sv.bpassign %82, %30 : i1
        sv.bpassign %83, %32 : i1
        sv.bpassign %84, %34 : i1
        sv.bpassign %85, %49 : i1
        sv.bpassign %86, %50 : i1
        sv.bpassign %87, %51 : i1
        sv.bpassign %88, %52 : i1
        sv.bpassign %89, %53 : i1
        sv.bpassign %90, %54 : i1
        sv.bpassign %91, %55 : i1
        sv.bpassign %65, %56 : i1
        sv.bpassign %66, %56 : i1
        sv.if %en0 {
            sv.bpassign %65, %data0_x : i1
            sv.bpassign %66, %0 : i1
            sv.bpassign %67, %23 : i1
        } else {
            sv.if %en1 {
                sv.bpassign %68, %26 : i1
                sv.bpassign %69, %28 : i1
                sv.bpassign %70, %30 : i1
                sv.bpassign %71, %32 : i1
                sv.bpassign %72, %34 : i1
                sv.bpassign %65, %data1_x : i1
                sv.bpassign %73, %36 : i1
                sv.bpassign %74, %38 : i1
                sv.bpassign %75, %40 : i1
                sv.bpassign %76, %42 : i1
                sv.bpassign %77, %44 : i1
                sv.bpassign %78, %46 : i1
                sv.bpassign %79, %48 : i1
                sv.bpassign %66, %0 : i1
                sv.bpassign %80, %25 : i1
                sv.bpassign %81, %27 : i1
                sv.bpassign %82, %29 : i1
                sv.bpassign %83, %31 : i1
                sv.bpassign %84, %33 : i1
                sv.bpassign %67, %23 : i1
                sv.bpassign %85, %49 : i1
                sv.bpassign %86, %50 : i1
                sv.bpassign %87, %51 : i1
                sv.bpassign %88, %52 : i1
                sv.bpassign %89, %53 : i1
                sv.bpassign %90, %54 : i1
                sv.bpassign %91, %55 : i1
            } else {
                sv.bpassign %67, %0 : i1
                sv.bpassign %85, %0 : i1
                sv.bpassign %86, %0 : i1
                sv.bpassign %87, %0 : i1
                sv.bpassign %88, %0 : i1
                sv.bpassign %89, %0 : i1
                sv.bpassign %90, %0 : i1
                sv.bpassign %91, %0 : i1
            }
        }
    }
    %92 = comb.concat %64, %63, %62, %61, %60, %59, %58 : i1, i1, i1, i1, i1, i1, i1
    hw.output %57, %92 : i1, i7
}
