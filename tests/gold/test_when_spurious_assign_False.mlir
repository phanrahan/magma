module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_spurious_assign_False(in %x: i8, in %y: i1, in %z: i2, in %CLK: i1, out O: !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>) {
        %0 = comb.extract %z from 0 : (i2) -> i1
        %1 = comb.extract %z from 1 : (i2) -> i1
        %2 = hw.constant 1 : i1
        %3 = hw.constant 1 : i8
        %5 = hw.constant -1 : i8
        %4 = comb.xor %5, %x : i8
        %8 = sv.reg : !hw.inout<i8>
        %6 = sv.read_inout %8 : !hw.inout<i8>
        %9 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %9 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %8, %x : i8
                } else {
                    sv.bpassign %8, %3 : i8
                }
            } else {
                sv.bpassign %8, %4 : i8
            }
        }
        %11 = sv.wire sym @test_when_spurious_assign_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %11, %6 : i8
        %10 = sv.read_inout %11 : !hw.inout<i8>
        %12 = hw.constant 1 : i1
        %14 = hw.constant -1 : i1
        %13 = comb.xor %14, %y : i1
        %17 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %17 : !hw.inout<i1>
        %18 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %18 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %1 {
                sv.bpassign %17, %y : i1
            } else {
                sv.bpassign %17, %13 : i1
            }
        }
        %20 = sv.wire sym @test_when_spurious_assign_False._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %20, %15 : i1
        %19 = sv.read_inout %20 : !hw.inout<i1>
        %21 = hw.struct_create (%10, %19) : !hw.struct<x: i8, y: i1>
        %22 = hw.struct_create (%x, %21) : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
        %24 = sv.reg name "Register_inst0" : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>>
        sv.alwaysff(posedge %CLK) {
            sv.if %0 {
                sv.passign %24, %22 : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
            }
        }
        %26 = hw.constant 0 : i8
        %28 = hw.constant 0 : i8
        %29 = hw.constant 0 : i1
        %27 = hw.struct_create (%28, %29) : !hw.struct<x: i8, y: i1>
        %25 = hw.struct_create (%26, %27) : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
        sv.initial {
            sv.bpassign %24, %25 : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
        }
        %23 = sv.read_inout %24 : !hw.inout<!hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>>
        %30 = comb.and %0, %1 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %10, %x) : i1, i8, i8
        %31 = comb.xor %14, %1 : i1
        %32 = comb.and %0, %31 : i1
        %33 = hw.constant 1 : i8
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %10, %33) : i1, i8, i8
        %34 = comb.xor %14, %0 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%34, %10, %4) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%1, %19, %y) : i1, i1, i1
        %35 = comb.xor %14, %1 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%35, %19, %13) : i1, i1, i1
        hw.output %23 : !hw.struct<x: i8, y: !hw.struct<x: i8, y: i1>>
    }
}
