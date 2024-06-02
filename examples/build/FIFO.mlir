module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Memory(in %RADDR: i2, in %CLK: i1, in %WADDR: i2, in %WDATA: !hw.struct<sign: i1, exponent: i8, significand: i23>, in %WE: i1, out RDATA: !hw.struct<sign: i1, exponent: i8, significand: i23>) {
        %0 = hw.struct_extract %WDATA["sign"] : !hw.struct<sign: i1, exponent: i8, significand: i23>
        %1 = hw.struct_extract %WDATA["exponent"] : !hw.struct<sign: i1, exponent: i8, significand: i23>
        %2 = comb.extract %1 from 0 : (i8) -> i1
        %3 = comb.extract %1 from 1 : (i8) -> i1
        %4 = comb.extract %1 from 2 : (i8) -> i1
        %5 = comb.extract %1 from 3 : (i8) -> i1
        %6 = comb.extract %1 from 4 : (i8) -> i1
        %7 = comb.extract %1 from 5 : (i8) -> i1
        %8 = comb.extract %1 from 6 : (i8) -> i1
        %9 = comb.extract %1 from 7 : (i8) -> i1
        %10 = hw.struct_extract %WDATA["significand"] : !hw.struct<sign: i1, exponent: i8, significand: i23>
        %11 = comb.extract %10 from 0 : (i23) -> i1
        %12 = comb.extract %10 from 1 : (i23) -> i1
        %13 = comb.extract %10 from 2 : (i23) -> i1
        %14 = comb.extract %10 from 3 : (i23) -> i1
        %15 = comb.extract %10 from 4 : (i23) -> i1
        %16 = comb.extract %10 from 5 : (i23) -> i1
        %17 = comb.extract %10 from 6 : (i23) -> i1
        %18 = comb.extract %10 from 7 : (i23) -> i1
        %19 = comb.extract %10 from 8 : (i23) -> i1
        %20 = comb.extract %10 from 9 : (i23) -> i1
        %21 = comb.extract %10 from 10 : (i23) -> i1
        %22 = comb.extract %10 from 11 : (i23) -> i1
        %23 = comb.extract %10 from 12 : (i23) -> i1
        %24 = comb.extract %10 from 13 : (i23) -> i1
        %25 = comb.extract %10 from 14 : (i23) -> i1
        %26 = comb.extract %10 from 15 : (i23) -> i1
        %27 = comb.extract %10 from 16 : (i23) -> i1
        %28 = comb.extract %10 from 17 : (i23) -> i1
        %29 = comb.extract %10 from 18 : (i23) -> i1
        %30 = comb.extract %10 from 19 : (i23) -> i1
        %31 = comb.extract %10 from 20 : (i23) -> i1
        %32 = comb.extract %10 from 21 : (i23) -> i1
        %33 = comb.extract %10 from 22 : (i23) -> i1
        %34 = comb.concat %33, %32, %31, %30, %29, %28, %27, %26, %25, %24, %23, %22, %21, %20, %19, %18, %17, %16, %15, %14, %13, %12, %11, %9, %8, %7, %6, %5, %4, %3, %2, %0 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %36 = sv.reg name "coreir_mem4x32_inst0" : !hw.inout<!hw.array<4xi32>>
        %37 = sv.array_index_inout %36[%RADDR] : !hw.inout<!hw.array<4xi32>>, i2
        %35 = sv.read_inout %37 : !hw.inout<i32>
        %38 = sv.array_index_inout %36[%WADDR] : !hw.inout<!hw.array<4xi32>>, i2
        sv.alwaysff(posedge %CLK) {
            sv.if %WE {
                sv.passign %38, %34 : i32
            }
        }
        %39 = comb.extract %35 from 0 : (i32) -> i1
        %40 = comb.extract %35 from 1 : (i32) -> i1
        %41 = comb.extract %35 from 2 : (i32) -> i1
        %42 = comb.extract %35 from 3 : (i32) -> i1
        %43 = comb.extract %35 from 4 : (i32) -> i1
        %44 = comb.extract %35 from 5 : (i32) -> i1
        %45 = comb.extract %35 from 6 : (i32) -> i1
        %46 = comb.extract %35 from 7 : (i32) -> i1
        %47 = comb.extract %35 from 8 : (i32) -> i1
        %48 = comb.concat %47, %46, %45, %44, %43, %42, %41, %40 : i1, i1, i1, i1, i1, i1, i1, i1
        %49 = comb.extract %35 from 9 : (i32) -> i1
        %50 = comb.extract %35 from 10 : (i32) -> i1
        %51 = comb.extract %35 from 11 : (i32) -> i1
        %52 = comb.extract %35 from 12 : (i32) -> i1
        %53 = comb.extract %35 from 13 : (i32) -> i1
        %54 = comb.extract %35 from 14 : (i32) -> i1
        %55 = comb.extract %35 from 15 : (i32) -> i1
        %56 = comb.extract %35 from 16 : (i32) -> i1
        %57 = comb.extract %35 from 17 : (i32) -> i1
        %58 = comb.extract %35 from 18 : (i32) -> i1
        %59 = comb.extract %35 from 19 : (i32) -> i1
        %60 = comb.extract %35 from 20 : (i32) -> i1
        %61 = comb.extract %35 from 21 : (i32) -> i1
        %62 = comb.extract %35 from 22 : (i32) -> i1
        %63 = comb.extract %35 from 23 : (i32) -> i1
        %64 = comb.extract %35 from 24 : (i32) -> i1
        %65 = comb.extract %35 from 25 : (i32) -> i1
        %66 = comb.extract %35 from 26 : (i32) -> i1
        %67 = comb.extract %35 from 27 : (i32) -> i1
        %68 = comb.extract %35 from 28 : (i32) -> i1
        %69 = comb.extract %35 from 29 : (i32) -> i1
        %70 = comb.extract %35 from 30 : (i32) -> i1
        %71 = comb.extract %35 from 31 : (i32) -> i1
        %72 = comb.concat %71, %70, %69, %68, %67, %66, %65, %64, %63, %62, %61, %60, %59, %58, %57, %56, %55, %54, %53, %52, %51, %50, %49 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %73 = hw.struct_create (%39, %48, %72) : !hw.struct<sign: i1, exponent: i8, significand: i23>
        hw.output %73 : !hw.struct<sign: i1, exponent: i8, significand: i23>
    }
    hw.module @FIFO(in %data_in_valid: i1, in %data_in_data: !hw.struct<sign: i1, exponent: i8, significand: i23>, in %data_out_ready: i1, in %CLK: i1, out data_in_ready: i1, out data_out_valid: i1, out data_out_data: !hw.struct<sign: i1, exponent: i8, significand: i23>) {
        %0 = hw.constant 1 : i3
        %2 = comb.add %1, %0 : i3
        %3 = hw.constant 1 : i1
        %4 = comb.and %data_out_ready, %3 : i1
        %6 = hw.array_create %2, %1 : i3
        %5 = hw.array_get %6[%4] : !hw.array<2xi3>, i1
        %7 = sv.reg name "Register_inst0" : !hw.inout<i3>
        sv.alwaysff(posedge %CLK) {
            sv.passign %7, %5 : i3
        }
        %8 = hw.constant 0 : i3
        sv.initial {
            sv.bpassign %7, %8 : i3
        }
        %1 = sv.read_inout %7 : !hw.inout<i3>
        %9 = comb.extract %1 from 0 : (i3) -> i1
        %10 = comb.extract %1 from 1 : (i3) -> i1
        %11 = comb.concat %10, %9 : i1, i1
        %12 = hw.constant 1 : i3
        %14 = comb.add %13, %12 : i3
        %17 = hw.constant -1 : i1
        %16 = comb.xor %17, %15 : i1
        %18 = comb.and %data_in_valid, %16 : i1
        %20 = hw.array_create %14, %13 : i3
        %19 = hw.array_get %20[%18] : !hw.array<2xi3>, i1
        %21 = sv.reg name "Register_inst1" : !hw.inout<i3>
        sv.alwaysff(posedge %CLK) {
            sv.passign %21, %19 : i3
        }
        sv.initial {
            sv.bpassign %21, %8 : i3
        }
        %13 = sv.read_inout %21 : !hw.inout<i3>
        %22 = comb.extract %13 from 0 : (i3) -> i1
        %23 = comb.extract %13 from 1 : (i3) -> i1
        %24 = comb.concat %23, %22 : i1, i1
        %25 = comb.icmp eq %11, %24 : i2
        %26 = comb.extract %1 from 2 : (i3) -> i1
        %27 = comb.extract %13 from 2 : (i3) -> i1
        %28 = comb.xor %26, %27 : i1
        %15 = comb.and %25, %28 : i1
        %29 = comb.xor %17, %15 : i1
        %30 = comb.concat %10, %9 : i1, i1
        %31 = comb.concat %23, %22 : i1, i1
        %32 = hw.instance "Memory_inst0" @Memory(RADDR: %30: i2, CLK: %CLK: i1, WADDR: %31: i2, WDATA: %data_in_data: !hw.struct<sign: i1, exponent: i8, significand: i23>, WE: %18: i1) -> (RDATA: !hw.struct<sign: i1, exponent: i8, significand: i23>)
        hw.output %29, %4, %32 : i1, i1, !hw.struct<sign: i1, exponent: i8, significand: i23>
    }
}
