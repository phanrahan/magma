module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Foo(%I: i1) -> () {
        sv.verbatim "always @(*) $display(\"%d\\n\", {{0}});" (%I) : i1
    }
    hw.module @Foo_unq1(%I: i1) -> () {
        sv.verbatim "always @(*) $display(\"%x\\n\", {{0}});" (%I) : i1
    }
    hw.module @inline_verilog2_uniquification(%I: i1) -> () {
        hw.instance "Foo_inst0" @Foo(I: %I: i1) -> ()
        hw.instance "Foo_inst1" @Foo_unq1(I: %I: i1) -> ()
    }
}
