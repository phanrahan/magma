module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Memory(in %RADDR: i2, in %CLK: i1, in %WADDR: i2, in %WDATA: !hw.struct<significand: i23>, in %WE: i1, out RDATA: !hw.struct<significand: i23>) {
        %0 = hw.struct_extract %WDATA["significand"] : !hw.struct<significand: i23>
        %2 = sv.reg name "coreir_mem4x23_inst0" : !hw.inout<!hw.array<4xi23>>
        %3 = sv.array_index_inout %2[%RADDR] : !hw.inout<!hw.array<4xi23>>, i2
        %1 = sv.read_inout %3 : !hw.inout<i23>
        %4 = sv.array_index_inout %2[%WADDR] : !hw.inout<!hw.array<4xi23>>, i2
        sv.alwaysff(posedge %CLK) {
            sv.if %WE {
                sv.passign %4, %0 : i23
            }
        }
        %5 = hw.struct_create (%1) : !hw.struct<significand: i23>
        hw.output %5 : !hw.struct<significand: i23>
    }
    hw.module @FIFO(in %data_in_valid: i1, in %data_in_data: !hw.struct<significand: i23>, in %data_out_ready: i1, in %CLK: i1, out data_in_ready: i1, out data_out_valid: i1, out data_out_data: !hw.struct<significand: i23>) {
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
        %32 = hw.instance "Memory_inst0" @Memory(RADDR: %30: i2, CLK: %CLK: i1, WADDR: %31: i2, WDATA: %data_in_data: !hw.struct<significand: i23>, WE: %18: i1) -> (RDATA: !hw.struct<significand: i23>)
        hw.output %29, %4, %32 : i1, i1, !hw.struct<significand: i23>
    }
}
