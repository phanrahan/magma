module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_inline_verilog_passthrough_wire(in %I: !hw.struct<x: i1, y: i4>, out O: !hw.struct<x: i1, y: i4>) {
        %0 = hw.struct_extract %I["y"] : !hw.struct<x: i1, y: i4>
        %1 = comb.extract %0 from 0 : (i4) -> i1
        %2 = comb.extract %0 from 1 : (i4) -> i1
        sv.verbatim "assert {{0}} == {{1}}" (%1, %2) : i1, i1
        %3 = comb.extract %0 from 2 : (i4) -> i1
        %4 = comb.concat %3, %2 : i1, i1
        %5 = comb.extract %0 from 3 : (i4) -> i1
        %6 = comb.concat %5, %3 : i1, i1
        sv.verbatim "assert {{0}} == {{1}}" (%4, %6) : i2, i2
        hw.output %I : !hw.struct<x: i1, y: i4>
    }
}
