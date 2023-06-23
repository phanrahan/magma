module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_tuple_bulk_resolve(%I_x: i8, %I_y_x_x: i8, %I_y_x_y: i8, %I_y_y_x: i8, %I_y_y_y: i8, %S: i2, %CLK: i1) -> (O_x: i8, O_y_x_x: i8, O_y_x_y: i8, O_y_y_x: i8, O_y_y_y: i8) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %11 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %11, %1 : i8
        }
        %12 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %11, %12 : i8
        }
        %6 = sv.read_inout %11 : !hw.inout<i8>
        %13 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %13, %2 : i8
        }
        %14 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %13, %14 : i8
        }
        %7 = sv.read_inout %13 : !hw.inout<i8>
        %15 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %15, %3 : i8
        }
        %16 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %15, %16 : i8
        }
        %8 = sv.read_inout %15 : !hw.inout<i8>
        %17 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %17, %4 : i8
        }
        %18 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %17, %18 : i8
        }
        %9 = sv.read_inout %17 : !hw.inout<i8>
        %19 = sv.reg name "y" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %19, %5 : i8
        }
        %20 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %19, %20 : i8
        }
        %10 = sv.read_inout %19 : !hw.inout<i8>
        %21 = comb.extract %S from 1 : (i2) -> i1
        %32 = sv.reg name "_WHEN_WIRE_109" : !hw.inout<i8>
        %27 = sv.read_inout %32 : !hw.inout<i8>
        %33 = sv.reg name "_WHEN_WIRE_110" : !hw.inout<i8>
        %28 = sv.read_inout %33 : !hw.inout<i8>
        %34 = sv.reg name "_WHEN_WIRE_111" : !hw.inout<i8>
        %29 = sv.read_inout %34 : !hw.inout<i8>
        %35 = sv.reg name "_WHEN_WIRE_112" : !hw.inout<i8>
        %30 = sv.read_inout %35 : !hw.inout<i8>
        %36 = sv.reg name "_WHEN_WIRE_113" : !hw.inout<i8>
        %31 = sv.read_inout %36 : !hw.inout<i8>
        %37 = sv.reg name "_WHEN_WIRE_114" : !hw.inout<i8>
        %1 = sv.read_inout %37 : !hw.inout<i8>
        %38 = sv.reg name "_WHEN_WIRE_115" : !hw.inout<i8>
        %2 = sv.read_inout %38 : !hw.inout<i8>
        %39 = sv.reg name "_WHEN_WIRE_116" : !hw.inout<i8>
        %3 = sv.read_inout %39 : !hw.inout<i8>
        %40 = sv.reg name "_WHEN_WIRE_117" : !hw.inout<i8>
        %4 = sv.read_inout %40 : !hw.inout<i8>
        %41 = sv.reg name "_WHEN_WIRE_118" : !hw.inout<i8>
        %5 = sv.read_inout %41 : !hw.inout<i8>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %32, %22 : i8
                sv.bpassign %37, %6 : i8
                sv.bpassign %35, %25 : i8
                sv.bpassign %36, %26 : i8
                sv.bpassign %33, %23 : i8
                sv.bpassign %34, %24 : i8
                sv.bpassign %38, %7 : i8
                sv.bpassign %39, %8 : i8
                sv.bpassign %40, %9 : i8
                sv.bpassign %41, %10 : i8
            } else {
                sv.bpassign %37, %22 : i8
                sv.bpassign %38, %23 : i8
                sv.bpassign %39, %24 : i8
                sv.bpassign %40, %25 : i8
                sv.bpassign %41, %26 : i8
                sv.if %21 {
                    sv.bpassign %32, %I_x : i8
                    sv.bpassign %35, %I_y_y_x : i8
                    sv.bpassign %36, %I_y_y_y : i8
                    sv.bpassign %33, %I_y_x_x : i8
                    sv.bpassign %34, %I_y_x_y : i8
                } else {
                    sv.bpassign %32, %22 : i8
                    sv.bpassign %35, %25 : i8
                    sv.bpassign %36, %26 : i8
                    sv.bpassign %33, %23 : i8
                    sv.bpassign %34, %24 : i8
                }
            }
        }
        %42 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %42, %27 : i8
        }
        sv.initial {
            sv.bpassign %42, %12 : i8
        }
        %22 = sv.read_inout %42 : !hw.inout<i8>
        %43 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %43, %28 : i8
        }
        sv.initial {
            sv.bpassign %43, %14 : i8
        }
        %23 = sv.read_inout %43 : !hw.inout<i8>
        %44 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %44, %29 : i8
        }
        sv.initial {
            sv.bpassign %44, %16 : i8
        }
        %24 = sv.read_inout %44 : !hw.inout<i8>
        %45 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %45, %30 : i8
        }
        sv.initial {
            sv.bpassign %45, %18 : i8
        }
        %25 = sv.read_inout %45 : !hw.inout<i8>
        %46 = sv.reg name "x" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %46, %31 : i8
        }
        sv.initial {
            sv.bpassign %46, %20 : i8
        }
        %26 = sv.read_inout %46 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_169: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %27, %22) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_170: assert property (({{0}}) |-> ({{{{1}}, {{2}}}, {{{3}}, {{4}}}} == {{{{5}}, {{6}}}, {{{7}}, {{8}}}}));" (%0, %31, %30, %29, %28, %26, %25, %24, %23) : i1, i8, i8, i8, i8, i8, i8, i8, i8
        sv.verbatim "WHEN_ASSERT_171: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %1, %6) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_172: assert property (({{0}}) |-> ({{{{1}}, {{2}}}, {{{3}}, {{4}}}} == {{{{5}}, {{6}}}, {{{7}}, {{8}}}}));" (%0, %5, %4, %3, %2, %10, %9, %8, %7) : i1, i8, i8, i8, i8, i8, i8, i8, i8
        %48 = hw.constant -1 : i1
        %47 = comb.xor %48, %0 : i1
        sv.verbatim "WHEN_ASSERT_173: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%47, %1, %22) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_174: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%47, %2, %23) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_175: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%47, %3, %24) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_176: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%47, %4, %25) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_177: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%47, %5, %26) : i1, i8, i8
        %49 = comb.and %47, %21 : i1
        sv.verbatim "WHEN_ASSERT_178: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%49, %27, %I_x) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_179: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%49, %30, %I_y_y_x) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_180: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%49, %31, %I_y_y_y) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_181: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%49, %28, %I_y_x_x) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_182: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%49, %29, %I_y_x_y) : i1, i8, i8
        %50 = comb.xor %48, %21 : i1
        %51 = comb.and %47, %50 : i1
        sv.verbatim "WHEN_ASSERT_183: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %27, %22) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_184: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %30, %25) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_185: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %31, %26) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_186: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %28, %23) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_187: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %29, %24) : i1, i8, i8
        hw.output %22, %23, %24, %25, %26 : i8, i8, i8, i8, i8
    }
}
