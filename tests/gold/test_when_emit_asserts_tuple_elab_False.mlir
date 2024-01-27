module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_emit_asserts_tuple_elab_False(in %I: !hw.array<2x!hw.struct<_0: i8, _1: i1>>, in %S: i1, in %CLK: i1, out O: !hw.struct<_0: i8, _1: i1>) {
        %1 = hw.constant 0 : i1
        %0 = hw.array_get %I[%1] : !hw.array<2x!hw.struct<_0: i8, _1: i1>>, i1
        %2 = hw.struct_extract %0["_1"] : !hw.struct<_0: i8, _1: i1>
        %5 = sv.reg : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        %4 = sv.read_inout %5 : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        sv.alwayscomb {
            sv.bpassign %5, %3 : !hw.struct<_0: i8, _1: i1>
            sv.if %S {
                sv.bpassign %5, %3 : !hw.struct<_0: i8, _1: i1>
            } else {
                sv.if %2 {
                    sv.bpassign %5, %3 : !hw.struct<_0: i8, _1: i1>
                }
            }
        }
        %7 = sv.wire sym @test_when_emit_asserts_tuple_elab_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        sv.assign %7, %4 : !hw.struct<_0: i8, _1: i1>
        %6 = sv.read_inout %7 : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        %8 = sv.reg name "Register_inst0" : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %8, %6 : !hw.struct<_0: i8, _1: i1>
        }
        %10 = hw.constant 0 : i8
        %11 = hw.constant 0 : i1
        %9 = hw.struct_create (%10, %11) : !hw.struct<_0: i8, _1: i1>
        sv.initial {
            sv.bpassign %8, %9 : !hw.struct<_0: i8, _1: i1>
        }
        %3 = sv.read_inout %8 : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %6, %3) : i1, !hw.struct<_0: i8, _1: i1>, !hw.struct<_0: i8, _1: i1>
        %13 = hw.constant -1 : i1
        %12 = comb.xor %13, %S : i1
        %14 = comb.and %12, %2 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %6, %3) : i1, !hw.struct<_0: i8, _1: i1>, !hw.struct<_0: i8, _1: i1>
        %15 = comb.or %S, %14 : i1
        %16 = comb.xor %13, %15 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%16, %6, %3) : i1, !hw.struct<_0: i8, _1: i1>, !hw.struct<_0: i8, _1: i1>
        hw.output %3 : !hw.struct<_0: i8, _1: i1>
    }
}
