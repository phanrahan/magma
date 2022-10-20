module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_protocol(%S: i1) -> (O: !hw.array<2xi1>) {
        %0 = hw.constant 0 : i1
        %1 = hw.constant 1 : i1
        %4 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %4, %0 : i1
                sv.bpassign %5, %0 : i1
            } else {
                sv.bpassign %4, %1 : i1
                sv.bpassign %5, %1 : i1
            }
        }
        %6 = comb.concat %3, %2 : i1, i1
        %8 = sv.wire sym @test_when_lazy_array_protocol.x {name="x"} : !hw.inout<i2>
        sv.assign %8, %6 : i2
        %7 = sv.read_inout %8 : !hw.inout<i2>
        hw.output %7 : i2
    }
}
