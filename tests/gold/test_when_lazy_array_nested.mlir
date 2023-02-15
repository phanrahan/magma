module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_nested(%S: i1) -> (O: !hw.array<2x!hw.struct<x: i1, y: i1>>) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 1 : i1
        %6 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %6 : !hw.inout<i1>
        %7 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %7 : !hw.inout<i1>
        %8 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %8 : !hw.inout<i1>
        %9 = sv.reg : !hw.inout<i1>
        %5 = sv.read_inout %9 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %6, %0 : i1
                sv.bpassign %7, %1 : i1
                sv.bpassign %8, %0 : i1
                sv.bpassign %9, %1 : i1
            } else {
                sv.bpassign %6, %1 : i1
                sv.bpassign %7, %0 : i1
                sv.bpassign %8, %1 : i1
                sv.bpassign %9, %0 : i1
            }
        }
        %10 = hw.struct_create (%2, %3) : !hw.struct<x: i1, y: i1>
        %11 = hw.struct_create (%4, %5) : !hw.struct<x: i1, y: i1>
        %12 = hw.array_create %10, %11 : !hw.struct<x: i1, y: i1>
        %14 = sv.wire sym @test_when_lazy_array_nested.x {name="x"} : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i1>>>
        sv.assign %14, %12 : !hw.array<2x!hw.struct<x: i1, y: i1>>
        %13 = sv.read_inout %14 : !hw.inout<!hw.array<2x!hw.struct<x: i1, y: i1>>>
        hw.output %13 : !hw.array<2x!hw.struct<x: i1, y: i1>>
    }
}
