module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_inline_verilog2_clock_output(%x: i1, %y: i1) -> () {
        sv.verbatim "Foo bar (.x({{0}}), .y({{1}}))" (%x, %y) : i1, i1
    }
}
