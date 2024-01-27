module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @ASSERT_ON_compile_guard(in %port_0: i1, in %port_1: i1, in %port_2: i4) {
        %0 = hw.constant 1 : i2
        %2 = comb.add %1, %0 : i2
        %3 = sv.reg name "Register_inst0" : !hw.inout<i2>
        sv.alwaysff(posedge %port_1) {
            sv.if %port_0 {
                sv.passign %3, %2 : i2
            }
        }
        %4 = hw.constant 0 : i2
        sv.initial {
            sv.bpassign %3, %4 : i2
        }
        %1 = sv.read_inout %3 : !hw.inout<i2>
        %5 = hw.constant 3 : i2
        %6 = comb.icmp eq %1, %5 : i2
        %8 = hw.constant -1 : i1
        %7 = comb.xor %8, %6 : i1
        %9 = hw.constant 3 : i4
        %10 = comb.icmp eq %port_2, %9 : i4
        %11 = comb.or %7, %10 : i1
        sv.verbatim "always @(*) begin\n\nassert ({{0}});\nend\n" (%11) : i1
    }
    hw.module @_Top(in %I: !hw.struct<valid: i1, data: i4>, in %CLK: i1, out O: i4) {
        %0 = hw.struct_extract %I["data"] : !hw.struct<valid: i1, data: i4>
        %2 = sv.reg name "Register_inst0" : !hw.inout<i4>
        sv.alwaysff(posedge %CLK) {
            sv.passign %2, %0 : i4
        }
        %3 = hw.constant 0 : i4
        sv.initial {
            sv.bpassign %2, %3 : i4
        }
        %1 = sv.read_inout %2 : !hw.inout<i4>
        %4 = hw.struct_extract %I["valid"] : !hw.struct<valid: i1, data: i4>
        sv.ifdef "ASSERT_ON" {
            hw.instance "ASSERT_ON_compile_guard" @ASSERT_ON_compile_guard(port_0: %4: i1, port_1: %CLK: i1, port_2: %1: i4) -> ()
        }
        hw.output %1 : i4
    }
}
