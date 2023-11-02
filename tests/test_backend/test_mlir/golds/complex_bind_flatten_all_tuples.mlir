module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @complex_bind_asserts(in %I_I: i1, in %O: i1, in %CLK: i1, in %I0: i1) {
        sv.verbatim "assert property (@(posedge CLK) {{1}} |-> ##1 {{0}});assert property ({{1}} |-> {{2}};" (%O, %I_I, %I0) : i1, i1, i1
    }
    hw.module @complex_bind(in %I_I: i1, in %CLK: i1, out O: i1) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I_I : i1
        %2 = comb.xor %1, %0 : i1
        %4 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %4, %2 : i1
        }
        %5 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %4, %5 : i1
        }
        %3 = sv.read_inout %4 : !hw.inout<i1>
        hw.instance "complex_bind_asserts_inst" sym @complex_bind.complex_bind_asserts_inst @complex_bind_asserts(I_I: %I_I: i1, O: %3: i1, CLK: %CLK: i1, I0: %0: i1) -> () {doNotPrint = true}
        hw.output %3 : i1
    }
    sv.bind #hw.innerNameRef<@complex_bind::@complex_bind.complex_bind_asserts_inst>
}
