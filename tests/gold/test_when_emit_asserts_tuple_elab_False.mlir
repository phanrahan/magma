module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_emit_asserts_tuple_elab_False(in %I: !hw.array<2x!hw.struct<_0: i8, _1: i1>>, in %S: i1, in %CLK: i1, out O: !hw.struct<_0: i8, _1: i1>) {
        %1 = hw.constant 0 : i1
        %0 = hw.array_get %I[%1] : !hw.array<2x!hw.struct<_0: i8, _1: i1>>, i1
        %2 = hw.struct_extract %0["_1"] : !hw.struct<_0: i8, _1: i1>
        %5 = sv.reg : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        %4 = sv.read_inout %5 : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        sv.alwayscomb {
            %8 = hw.struct_create (%6, %7) : !hw.struct<_0: i8, _1: i1>
            sv.bpassign %5, %8 : !hw.struct<_0: i8, _1: i1>
            sv.if %S {
                %9 = hw.struct_create (%6, %7) : !hw.struct<_0: i8, _1: i1>
                sv.bpassign %5, %9 : !hw.struct<_0: i8, _1: i1>
            } else {
                sv.if %2 {
                    %10 = hw.struct_create (%6, %7) : !hw.struct<_0: i8, _1: i1>
                    sv.bpassign %5, %10 : !hw.struct<_0: i8, _1: i1>
                }
            }
        }
        %6 = hw.struct_extract %3["_0"] : !hw.struct<_0: i8, _1: i1>
        %7 = hw.struct_extract %3["_1"] : !hw.struct<_0: i8, _1: i1>
        %11 = hw.struct_extract %4["_0"] : !hw.struct<_0: i8, _1: i1>
        %13 = sv.wire sym @test_when_emit_asserts_tuple_elab_False._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i8>
        sv.assign %13, %11 : i8
        %12 = sv.read_inout %13 : !hw.inout<i8>
        %14 = hw.struct_extract %4["_1"] : !hw.struct<_0: i8, _1: i1>
        %16 = sv.wire sym @test_when_emit_asserts_tuple_elab_False._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %16, %14 : i1
        %15 = sv.read_inout %16 : !hw.inout<i1>
        %17 = hw.struct_create (%12, %15) : !hw.struct<_0: i8, _1: i1>
        %18 = sv.reg name "Register_inst0" : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %18, %17 : !hw.struct<_0: i8, _1: i1>
        }
        %20 = hw.constant 0 : i8
        %21 = hw.constant 0 : i1
        %19 = hw.struct_create (%20, %21) : !hw.struct<_0: i8, _1: i1>
        sv.initial {
            sv.bpassign %18, %19 : !hw.struct<_0: i8, _1: i1>
        }
        %3 = sv.read_inout %18 : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        %22 = hw.struct_create (%12, %15) : !hw.struct<_0: i8, _1: i1>
        %24 = sv.wire sym @test_when_emit_asserts_tuple_elab_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        sv.assign %24, %22 : !hw.struct<_0: i8, _1: i1>
        %23 = sv.read_inout %24 : !hw.inout<!hw.struct<_0: i8, _1: i1>>
        %25 = hw.struct_extract %23["_1"] : !hw.struct<_0: i8, _1: i1>
        %26 = hw.struct_extract %23["_0"] : !hw.struct<_0: i8, _1: i1>
        %27 = hw.struct_extract %3["_1"] : !hw.struct<_0: i8, _1: i1>
        %28 = hw.struct_extract %3["_0"] : !hw.struct<_0: i8, _1: i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%S, %25, %26, %27, %28) : i1, i1, i8, i1, i8
        %30 = hw.constant -1 : i1
        %29 = comb.xor %30, %S : i1
        %31 = comb.and %29, %2 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%31, %12, %28) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%31, %15, %27) : i1, i1, i1
        %32 = comb.xor %30, %31 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %12, %28) : i1, i8, i8
        %33 = comb.xor %30, %31 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%33, %15, %27) : i1, i1, i1
        hw.output %3 : !hw.struct<_0: i8, _1: i1>
    }
}
