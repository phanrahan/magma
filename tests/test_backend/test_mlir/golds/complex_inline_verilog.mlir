module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @complex_inline_verilog(%I: i12, %CLK: i1) -> (O: i12) {
        %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i12>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %I : i12
        }
        %2 = hw.constant 0 : i12
        sv.initial {
            sv.bpassign %1, %2 : i12
        }
        %0 = sv.read_inout %1 : !hw.inout<i12>
        %3 = comb.extract %I from 0 : (i12) -> i1
        %5 = sv.wire sym @complex_inline_verilog._magma_inline_wire0 {name="_magma_inline_wire0"} : !hw.inout<i1>
        sv.assign %5, %3 : i1
        %4 = sv.read_inout %5 : !hw.inout<i1>
        %6 = comb.extract %0 from 0 : (i12) -> i1
        %8 = sv.wire sym @complex_inline_verilog._magma_inline_wire1 {name="_magma_inline_wire1"} : !hw.inout<i1>
        sv.assign %8, %6 : i1
        %7 = sv.read_inout %8 : !hw.inout<i1>
        %9 = comb.extract %I from 1 : (i12) -> i1
        %11 = sv.wire sym @complex_inline_verilog._magma_inline_wire2 {name="_magma_inline_wire2"} : !hw.inout<i1>
        sv.assign %11, %9 : i1
        %10 = sv.read_inout %11 : !hw.inout<i1>
        %12 = comb.extract %0 from 1 : (i12) -> i1
        %14 = sv.wire sym @complex_inline_verilog._magma_inline_wire3 {name="_magma_inline_wire3"} : !hw.inout<i1>
        sv.assign %14, %12 : i1
        %13 = sv.read_inout %14 : !hw.inout<i1>
        %15 = comb.extract %I from 2 : (i12) -> i1
        %17 = sv.wire sym @complex_inline_verilog._magma_inline_wire4 {name="_magma_inline_wire4"} : !hw.inout<i1>
        sv.assign %17, %15 : i1
        %16 = sv.read_inout %17 : !hw.inout<i1>
        %18 = comb.extract %0 from 2 : (i12) -> i1
        %20 = sv.wire sym @complex_inline_verilog._magma_inline_wire5 {name="_magma_inline_wire5"} : !hw.inout<i1>
        sv.assign %20, %18 : i1
        %19 = sv.read_inout %20 : !hw.inout<i1>
        %21 = comb.extract %I from 3 : (i12) -> i1
        %23 = sv.wire sym @complex_inline_verilog._magma_inline_wire6 {name="_magma_inline_wire6"} : !hw.inout<i1>
        sv.assign %23, %21 : i1
        %22 = sv.read_inout %23 : !hw.inout<i1>
        %24 = comb.extract %0 from 3 : (i12) -> i1
        %26 = sv.wire sym @complex_inline_verilog._magma_inline_wire7 {name="_magma_inline_wire7"} : !hw.inout<i1>
        sv.assign %26, %24 : i1
        %25 = sv.read_inout %26 : !hw.inout<i1>
        %27 = comb.extract %I from 4 : (i12) -> i1
        %29 = sv.wire sym @complex_inline_verilog._magma_inline_wire8 {name="_magma_inline_wire8"} : !hw.inout<i1>
        sv.assign %29, %27 : i1
        %28 = sv.read_inout %29 : !hw.inout<i1>
        %30 = comb.extract %0 from 4 : (i12) -> i1
        %32 = sv.wire sym @complex_inline_verilog._magma_inline_wire9 {name="_magma_inline_wire9"} : !hw.inout<i1>
        sv.assign %32, %30 : i1
        %31 = sv.read_inout %32 : !hw.inout<i1>
        %33 = comb.extract %I from 5 : (i12) -> i1
        %35 = sv.wire sym @complex_inline_verilog._magma_inline_wire10 {name="_magma_inline_wire10"} : !hw.inout<i1>
        sv.assign %35, %33 : i1
        %34 = sv.read_inout %35 : !hw.inout<i1>
        %36 = comb.extract %0 from 5 : (i12) -> i1
        %38 = sv.wire sym @complex_inline_verilog._magma_inline_wire11 {name="_magma_inline_wire11"} : !hw.inout<i1>
        sv.assign %38, %36 : i1
        %37 = sv.read_inout %38 : !hw.inout<i1>
        %39 = comb.extract %I from 6 : (i12) -> i1
        %41 = sv.wire sym @complex_inline_verilog._magma_inline_wire12 {name="_magma_inline_wire12"} : !hw.inout<i1>
        sv.assign %41, %39 : i1
        %40 = sv.read_inout %41 : !hw.inout<i1>
        %42 = comb.extract %0 from 6 : (i12) -> i1
        %44 = sv.wire sym @complex_inline_verilog._magma_inline_wire13 {name="_magma_inline_wire13"} : !hw.inout<i1>
        sv.assign %44, %42 : i1
        %43 = sv.read_inout %44 : !hw.inout<i1>
        %45 = comb.extract %I from 7 : (i12) -> i1
        %47 = sv.wire sym @complex_inline_verilog._magma_inline_wire14 {name="_magma_inline_wire14"} : !hw.inout<i1>
        sv.assign %47, %45 : i1
        %46 = sv.read_inout %47 : !hw.inout<i1>
        %48 = comb.extract %0 from 7 : (i12) -> i1
        %50 = sv.wire sym @complex_inline_verilog._magma_inline_wire15 {name="_magma_inline_wire15"} : !hw.inout<i1>
        sv.assign %50, %48 : i1
        %49 = sv.read_inout %50 : !hw.inout<i1>
        %51 = comb.extract %I from 8 : (i12) -> i1
        %53 = sv.wire sym @complex_inline_verilog._magma_inline_wire16 {name="_magma_inline_wire16"} : !hw.inout<i1>
        sv.assign %53, %51 : i1
        %52 = sv.read_inout %53 : !hw.inout<i1>
        %54 = comb.extract %0 from 8 : (i12) -> i1
        %56 = sv.wire sym @complex_inline_verilog._magma_inline_wire17 {name="_magma_inline_wire17"} : !hw.inout<i1>
        sv.assign %56, %54 : i1
        %55 = sv.read_inout %56 : !hw.inout<i1>
        %57 = comb.extract %I from 9 : (i12) -> i1
        %59 = sv.wire sym @complex_inline_verilog._magma_inline_wire18 {name="_magma_inline_wire18"} : !hw.inout<i1>
        sv.assign %59, %57 : i1
        %58 = sv.read_inout %59 : !hw.inout<i1>
        %60 = comb.extract %0 from 9 : (i12) -> i1
        %62 = sv.wire sym @complex_inline_verilog._magma_inline_wire19 {name="_magma_inline_wire19"} : !hw.inout<i1>
        sv.assign %62, %60 : i1
        %61 = sv.read_inout %62 : !hw.inout<i1>
        %63 = comb.extract %I from 10 : (i12) -> i1
        %65 = sv.wire sym @complex_inline_verilog._magma_inline_wire20 {name="_magma_inline_wire20"} : !hw.inout<i1>
        sv.assign %65, %63 : i1
        %64 = sv.read_inout %65 : !hw.inout<i1>
        %66 = comb.extract %0 from 10 : (i12) -> i1
        %68 = sv.wire sym @complex_inline_verilog._magma_inline_wire21 {name="_magma_inline_wire21"} : !hw.inout<i1>
        sv.assign %68, %66 : i1
        %67 = sv.read_inout %68 : !hw.inout<i1>
        %69 = comb.extract %I from 11 : (i12) -> i1
        %71 = sv.wire sym @complex_inline_verilog._magma_inline_wire22 {name="_magma_inline_wire22"} : !hw.inout<i1>
        sv.assign %71, %69 : i1
        %70 = sv.read_inout %71 : !hw.inout<i1>
        %72 = comb.extract %0 from 11 : (i12) -> i1
        %74 = sv.wire sym @complex_inline_verilog._magma_inline_wire23 {name="_magma_inline_wire23"} : !hw.inout<i1>
        sv.assign %74, %72 : i1
        %73 = sv.read_inout %74 : !hw.inout<i1>
        sv.verbatim "assert property (@(posedge CLK) {{0}} |-> ##1 {{1}});\nassert property (@(posedge CLK) {{2}} |-> ##1 {{3}});\nassert property (@(posedge CLK) {{4}} |-> ##1 {{5}});\nassert property (@(posedge CLK) {{6}} |-> ##1 {{7}});\nassert property (@(posedge CLK) {{8}} |-> ##1 {{9}});\nassert property (@(posedge CLK) {{10}} |-> ##1 {{11}});\nassert property (@(posedge CLK) {{12}} |-> ##1 {{13}});\nassert property (@(posedge CLK) {{14}} |-> ##1 {{15}});\nassert property (@(posedge CLK) {{16}} |-> ##1 {{17}});\nassert property (@(posedge CLK) {{18}} |-> ##1 {{19}});\nassert property (@(posedge CLK) {{20}} |-> ##1 {{21}});\nassert property (@(posedge CLK) {{22}} |-> ##1 {{23}});" (%4, %7, %10, %13, %16, %19, %22, %25, %28, %31, %34, %37, %40, %43, %46, %49, %52, %55, %58, %61, %64, %67, %70, %73) : i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1, i1
        %76 = sv.wire sym @complex_inline_verilog._magma_inline_wire24 {name="_magma_inline_wire24"} : !hw.inout<i12>
        sv.assign %76, %I : i12
        %75 = sv.read_inout %76 : !hw.inout<i12>
        sv.verbatim "// A fun{k}y comment with {{0}}" (%75) : i12
        hw.output %0 : i12
    }
}
