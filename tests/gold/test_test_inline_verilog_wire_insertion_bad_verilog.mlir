module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_inline_verilog_wire_insertion_bad_verilog(in %I: i32, out O: i1) {
        %0 = comb.extract %I from 0 : (i32) -> i1
        sv.verbatim "`ifdef LOGGING_ON"
        sv.verbatim "$display(\"%x\", {{0}});" (%0) : i1
        sv.verbatim "`endif LOGGING_ON"
        hw.output %0 : i1
    }
}
