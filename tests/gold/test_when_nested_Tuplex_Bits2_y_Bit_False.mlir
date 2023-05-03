module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_Tuplex_Bits2_y_Bit_False(%I: !hw.array<2x!hw.struct<x: i2, y: i1>>, %S: i1) -> (O: !hw.struct<x: i2, y: i1>) {
        %1 = hw.constant 1 : i1
        %0 = hw.array_get %I[%1] : !hw.array<2x!hw.struct<x: i2, y: i1>>, i1
        %3 = hw.constant 0 : i1
        %2 = hw.array_get %I[%3] : !hw.array<2x!hw.struct<x: i2, y: i1>>, i1
        %5 = sv.reg : !hw.inout<!hw.struct<x: i2, y: i1>>
        %4 = sv.read_inout %5 : !hw.inout<!hw.struct<x: i2, y: i1>>
        sv.alwayscomb {
            sv.bpassign %5, %0 : !hw.struct<x: i2, y: i1>
            sv.if %S {
                sv.bpassign %5, %2 : !hw.struct<x: i2, y: i1>
            }
        }
        hw.output %4 : !hw.struct<x: i2, y: i1>
    }
}
