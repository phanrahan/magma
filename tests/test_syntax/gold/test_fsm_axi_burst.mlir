module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Memory(in %RADDR: i32, in %CLK: i1, out RDATA: i32) {
        %0 = hw.constant 0 : i32
        %1 = hw.constant 0 : i32
        %2 = hw.constant 0 : i1
        %4 = sv.reg name "coreir_mem4294967296x32_inst0" : !hw.inout<!hw.array<4294967296xi32>>
        %5 = sv.array_index_inout %4[%RADDR] : !hw.inout<!hw.array<4294967296xi32>>, i32
        %3 = sv.read_inout %5 : !hw.inout<i32>
        %6 = sv.array_index_inout %4[%0] : !hw.inout<!hw.array<4294967296xi32>>, i32
        sv.alwaysff(posedge %CLK) {
            sv.if %2 {
                sv.passign %6, %1 : i32
            }
        }
        hw.output %3 : i32
    }
    hw.module @AXIBurstReader(in %ARVALID: i1, in %ARADDR: i32, in %ARSIZE: i3, in %ARLEN: i8, in %RREADY: i1, in %CLK: i1, out ARREADY: i1, out RVALID: i1, out RLAST: i1, out RDATA: i32) {
        %1 = hw.struct_create (%0) : !hw.struct<tag: i1>
        %3 = sv.reg name "Register_inst0" : !hw.inout<!hw.struct<tag: i1>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %1 : !hw.struct<tag: i1>
        }
        %5 = hw.constant 0 : i1
        %4 = hw.struct_create (%5) : !hw.struct<tag: i1>
        sv.initial {
            sv.bpassign %3, %4 : !hw.struct<tag: i1>
        }
        %2 = sv.read_inout %3 : !hw.inout<!hw.struct<tag: i1>>
        %6 = hw.struct_extract %2["tag"] : !hw.struct<tag: i1>
        %7 = hw.constant 0 : i1
        %8 = comb.icmp eq %6, %7 : i1
        %9 = hw.constant 0 : i1
        %12 = sv.reg name "Register_inst1" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %12, %10 : i1
        }
        %13 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %12, %13 : i1
        }
        %11 = sv.read_inout %12 : !hw.inout<i1>
        %14 = hw.constant 1 : i1
        %17 = sv.reg name "Register_inst2" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %17, %15 : i1
        }
        sv.initial {
            sv.bpassign %17, %13 : i1
        }
        %16 = sv.read_inout %17 : !hw.inout<i1>
        %20 = sv.reg name "Register_inst3" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %20, %18 : i8
        }
        %21 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %20, %21 : i8
        }
        %19 = sv.read_inout %20 : !hw.inout<i8>
        %24 = sv.reg name "len_reg" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %24, %22 : i8
        }
        %25 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %24, %25 : i8
        }
        %23 = sv.read_inout %24 : !hw.inout<i8>
        %28 = sv.reg name "Register_inst4" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %28, %26 : i8
        }
        sv.initial {
            sv.bpassign %28, %21 : i8
        }
        %27 = sv.read_inout %28 : !hw.inout<i8>
        %29 = hw.constant 1 : i8
        %30 = comb.add %27, %29 : i8
        %31 = hw.constant 0 : i8
        %34 = sv.reg name "Register_inst5" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %34, %32 : i1
        }
        sv.initial {
            sv.bpassign %34, %13 : i1
        }
        %33 = sv.read_inout %34 : !hw.inout<i1>
        %35 = hw.constant 1 : i8
        %36 = comb.add %27, %35 : i8
        %38 = hw.constant -1 : i1
        %37 = comb.xor %38, %RREADY : i1
        %39 = comb.icmp ult %19, %27 : i8
        %42 = sv.reg name "addr_reg" : !hw.inout<i32>
        sv.alwaysff(posedge %CLK) {
            sv.passign %42, %40 : i32
        }
        %43 = hw.constant 0 : i32
        sv.initial {
            sv.bpassign %42, %43 : i32
        }
        %41 = sv.read_inout %42 : !hw.inout<i32>
        %44 = comb.extract %27 from 0 : (i8) -> i1
        %45 = comb.extract %27 from 1 : (i8) -> i1
        %46 = comb.extract %27 from 2 : (i8) -> i1
        %47 = comb.extract %27 from 3 : (i8) -> i1
        %48 = comb.extract %27 from 4 : (i8) -> i1
        %49 = comb.extract %27 from 5 : (i8) -> i1
        %50 = comb.extract %27 from 6 : (i8) -> i1
        %51 = comb.extract %27 from 7 : (i8) -> i1
        %52 = hw.constant 0 : i1
        %53 = hw.constant 0 : i1
        %54 = hw.constant 0 : i1
        %55 = hw.constant 0 : i1
        %56 = hw.constant 0 : i1
        %57 = hw.constant 0 : i1
        %58 = hw.constant 0 : i1
        %59 = hw.constant 0 : i1
        %60 = hw.constant 0 : i1
        %61 = hw.constant 0 : i1
        %62 = hw.constant 0 : i1
        %63 = hw.constant 0 : i1
        %64 = hw.constant 0 : i1
        %65 = hw.constant 0 : i1
        %66 = hw.constant 0 : i1
        %67 = hw.constant 0 : i1
        %68 = hw.constant 0 : i1
        %69 = hw.constant 0 : i1
        %70 = hw.constant 0 : i1
        %71 = hw.constant 0 : i1
        %72 = hw.constant 0 : i1
        %73 = hw.constant 0 : i1
        %74 = hw.constant 0 : i1
        %75 = hw.constant 0 : i1
        %76 = comb.concat %75, %74, %73, %72, %71, %70, %69, %68, %67, %66, %65, %64, %63, %62, %61, %60, %59, %58, %57, %56, %55, %54, %53, %52, %51, %50, %49, %48, %47, %46, %45, %44 : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %77 = comb.add %41, %76 : i32
        %78 = hw.constant 1 : i8
        %79 = comb.sub %23, %78 : i8
        %80 = comb.icmp eq %27, %79 : i8
        %81 = hw.constant 0 : i1
        %82 = hw.constant 0 : i32
        %85 = sv.reg name "size_reg" : !hw.inout<i3>
        sv.alwaysff(posedge %CLK) {
            sv.passign %85, %83 : i3
        }
        %86 = hw.constant 0 : i3
        sv.initial {
            sv.bpassign %85, %86 : i3
        }
        %84 = sv.read_inout %85 : !hw.inout<i3>
        %91 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %91 : !hw.inout<i1>
        %92 = sv.reg : !hw.inout<i32>
        %40 = sv.read_inout %92 : !hw.inout<i32>
        %93 = sv.reg : !hw.inout<i3>
        %83 = sv.read_inout %93 : !hw.inout<i3>
        %94 = sv.reg : !hw.inout<i8>
        %22 = sv.read_inout %94 : !hw.inout<i8>
        %95 = sv.reg : !hw.inout<i1>
        %87 = sv.read_inout %95 : !hw.inout<i1>
        %96 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %96 : !hw.inout<i1>
        %97 = sv.reg : !hw.inout<i8>
        %18 = sv.read_inout %97 : !hw.inout<i8>
        %98 = sv.reg : !hw.inout<i8>
        %26 = sv.read_inout %98 : !hw.inout<i8>
        %99 = sv.reg : !hw.inout<i1>
        %32 = sv.read_inout %99 : !hw.inout<i1>
        %100 = sv.reg : !hw.inout<i32>
        %88 = sv.read_inout %100 : !hw.inout<i32>
        %101 = sv.reg : !hw.inout<i1>
        %89 = sv.read_inout %101 : !hw.inout<i1>
        %102 = sv.reg : !hw.inout<i1>
        %90 = sv.read_inout %102 : !hw.inout<i1>
        %103 = sv.reg : !hw.inout<i1>
        %0 = sv.read_inout %103 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %91, %9 : i1
            sv.bpassign %95, %9 : i1
            sv.bpassign %96, %9 : i1
            sv.bpassign %97, %19 : i8
            sv.bpassign %98, %30 : i8
            sv.bpassign %99, %9 : i1
            sv.bpassign %101, %9 : i1
            sv.bpassign %102, %9 : i1
            sv.bpassign %100, %82 : i32
            sv.bpassign %92, %41 : i32
            sv.bpassign %93, %84 : i3
            sv.bpassign %94, %23 : i8
            sv.bpassign %103, %6 : i1
            sv.if %8 {
                sv.bpassign %91, %ARVALID : i1
                sv.if %11 {
                    sv.bpassign %92, %ARADDR : i32
                    sv.bpassign %93, %ARSIZE : i3
                    sv.bpassign %94, %ARLEN : i8
                    sv.bpassign %95, %14 : i1
                    sv.bpassign %96, %14 : i1
                    sv.if %16 {
                        sv.bpassign %97, %23 : i8
                        sv.bpassign %98, %31 : i8
                        sv.bpassign %99, %14 : i1
                        sv.if %33 {
                            sv.bpassign %98, %36 : i8
                            sv.if %37 {
                                sv.bpassign %98, %27 : i8
                            }
                            sv.if %39 {
                                sv.bpassign %100, %77 : i32
                                sv.bpassign %101, %14 : i1
                                sv.bpassign %102, %80 : i1
                            } else {
                                sv.bpassign %103, %81 : i1
                            }
                        }
                    }
                }
            }
        }
        %104 = hw.instance "mem" @Memory(RADDR: %88: i32, CLK: %CLK: i1) -> (RDATA: i32)
        hw.output %87, %89, %90, %104 : i1, i1, i1, i32
    }
}
