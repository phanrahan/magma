module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_bind_asserts(in %I: i1, in %O: i1, in %CLK: i1) attributes {output_filelist = #hw.output_filelist<"simple_bind_bind_files.list">} {
        sv.verbatim "assert property (@(posedge CLK) {{1}} |-> ##1 {{0}});" (%O, %I) : i1, i1
    }
    hw.module @simple_bind(in %I: i1, in %CLK: i1, out O: i1) {
        %1 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %I : i1
        }
        %2 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %1, %2 : i1
        }
        %0 = sv.read_inout %1 : !hw.inout<i1>
        hw.instance "simple_bind_asserts_inst0" sym @simple_bind.simple_bind_asserts_inst0 @simple_bind_asserts(I: %I: i1, O: %0: i1, CLK: %CLK: i1) -> () {doNotPrint = true}
        hw.output %0 : i1
    }
    sv.bind #hw.innerNameRef<@simple_bind::@simple_bind.simple_bind_asserts_inst0>
}
