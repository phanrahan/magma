module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @complex_bind_asserts(%I: !hw.struct<I: i1>, %O: i1, %CLK: i1, %I0: i1) -> () {
        %0 = hw.struct_extract %I["I"] : !hw.struct<I: i1>
        sv.verbatim "assert property (@(posedge CLK) {{1}} |-> ##1 {{0}});assert property ({{1}} |-> {{2}};" (%O, %0, %I0) : i1, i1, i1
    }
    hw.module @complex_bind(%I: !hw.struct<I: i1>, %CLK: i1) -> (O: i1) {
        %0 = hw.struct_extract %I["I"] : !hw.struct<I: i1>
        %2 = hw.constant -1 : i1
        %1 = comb.xor %2, %0 : i1
        %3 = comb.xor %2, %1 : i1
        %5 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %5, %3 : i1
        }
        %6 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %5, %6 : i1
        }
        %4 = sv.read_inout %5 : !hw.inout<i1>
        hw.instance "complex_bind_asserts_inst" sym @complex_bind.complex_bind_asserts_inst @complex_bind_asserts(I: %I: !hw.struct<I: i1>, O: %4: i1, CLK: %CLK: i1, I0: %1: i1) -> () {doNotPrint = true}
        hw.output %4 : i1
    }
    sv.bind #hw.innerNameRef<@complex_bind::@complex_bind.complex_bind_asserts_inst>
}
