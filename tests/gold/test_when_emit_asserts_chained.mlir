module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_chained(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 1 : (i2) -> i1
        %1 = comb.extract %S from 0 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %7 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %7 : !hw.inout<i1>
        %8 = sv.reg : !hw.inout<i1>
        %5 = sv.read_inout %8 : !hw.inout<i1>
        %9 = sv.reg : !hw.inout<i1>
        %6 = sv.read_inout %9 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %9, %2 : i1
            sv.if %1 {
                sv.bpassign %9, %3 : i1
            }
        }
        %11 = hw.constant -1 : i1
        %10 = comb.xor %11, %6 : i1
        %15 = sv.reg : !hw.inout<i1>
        %12 = sv.read_inout %15 : !hw.inout<i1>
        %16 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %17 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %17, %6 : i1
            sv.if %0 {
                sv.bpassign %17, %10 : i1
            }
        }
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %14, %10) : i1, i1, i1
        %18 = comb.xor %11, %0 : i1
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%18, %14, %6) : i1, i1, i1
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%1, %6, %3) : i1, i1, i1
        %19 = comb.xor %11, %1 : i1
        sv.verbatim "always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%19, %6, %2) : i1, i1, i1
        hw.output %14 : i1
    }
}
