module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_inline_verilog_clock_output(in %x: i1, in %y: i1) {
        sv.verbatim "Foo bar (.x({{0}}), .y({{1}}))" (%x, %y) : i1, i1
    }
}